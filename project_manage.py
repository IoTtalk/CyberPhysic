import random
import requests
import tornado.web
import json

import config

project_set = {}

'''
{'p_id':{
    'name':
    'input_device_info':{
        'dm_name': null,
        'dm_id': null,
        'do_id': 0,
        'df_list': [{'id':df_id, 'name':df_name}],
    },
    'output_device_info':{
        'dm_name': null,
        'dm_id': null,
        'do_id': 0,
        'df_list':[{'id':df_id, 'name':df_name}],
        'mac_addr': null,
    },
    'na_id_list':[],
    'fn_id_list':[], 
    },
}
'''

def create_project_handler(odm_name):
    new_proj_name = check_project_name(odm_name)
    data = {'p_name': new_proj_name, 'p_pwd': ''}
    new_p_id = post_to_ccm('/new_project', data)
    project_set[new_p_id] = {'name': new_proj_name, 'input_device_info':{}, 'output_device_info':{}, 'na_id_list':[], 'fn_id_list':[]}
    
    get_model_info(new_p_id, odm_name, "out")
    get_model_info(new_p_id, "Remote_control_"+odm_name,"in")
    reload_data(new_p_id)
    create_connection(new_p_id)

    print(project_set)
    return new_p_id


def check_project_name(odm_name):
    proj_name = 'CyberPhysic_'+odm_name+'_'+str(random.randint(1,1000))
    data = {'project_name': proj_name}
    response = post_to_ccm('/check_project_name_is_exist', data)

    if response['status'] == 'ok':
        if response['is_exist']:
            check_project_name()
        else:
            return proj_name


def get_model_info(new_p_id, model_name, in_out):
    model_info = {'model_name':model_name, 'p_id':new_p_id};
    data = {'model_info': json.dumps(model_info)}
    response = post_to_ccm('/get_model_info', data)

    def create_feature_list(name, idf_list, odf_list, model_id):
        project_set[new_p_id][name]['dm_name'] = model_name;
        project_set[new_p_id][name]['dm_id'] = model_id;
        return {
            'idf_list': idf_list,
            'odf_list': odf_list,
            'model_name': response['model_name'],
            'do_id': 0,
            'p_id': new_p_id,
        }

    if in_out == 'out':
        feature_list = create_feature_list('output_device_info', [], response['odf'], response['model_id'])
    else:
        feature_list = create_feature_list('input_device_info', response['idf'], [], response['model_id'])
    data = {'model_info': json.dumps(feature_list)}
    response = post_to_ccm('/save_device_object_info', data)


def reload_data(new_p_id): 
    data = {'p_id': new_p_id}
    response = post_to_ccm('/reload_data', data)
    in_device_info = response['in_device'][0]
    out_device_info = response['out_device'][0]

    # save input_device_info
    project_set[new_p_id]['input_device_info']['do_id'] = in_device_info['in_do_id']
    project_set[new_p_id]['input_device_info']['df_list'] = []
    for idf_info in in_device_info['p_idf_list']:
        # get df parameter
        data = {'model_info':json.dumps({'df_name': idf_info[0],'dm_id': project_set[new_p_id]['input_device_info']['dm_id']})}
        response = post_to_ccm('/get_device_feature_info', data)
        project_set[new_p_id]['input_device_info']['df_list'].append({'id':idf_info[1],'name':idf_info[0],'parameter':response['df_parameter']})

    #save output_device_info
    project_set[new_p_id]['output_device_info']['do_id'] = out_device_info['out_do_id']
    project_set[new_p_id]['output_device_info']['df_list'] = []
    for odf_info in out_device_info['p_odf_list']:
        project_set[new_p_id]['output_device_info']['df_list'].append({'id':odf_info[1],'name':odf_info[0]})

# create connection between idf and odfs(1 to n)
def create_connection(new_p_id):
    for i in range(len(project_set[new_p_id]['output_device_info']['df_list'])):
        
        # this is for multi-idf and idf to odf is 1 to 1
        connect_info = ["Join "+str(i+1),i,project_set[new_p_id]['input_device_info']['df_list'][i]['id'],project_set[new_p_id]['output_device_info']['df_list'][i]['id']];
        
        '''
        this is for idf to odf 1 to n
        connect_info = ["Join "+str(i+1),i,project_set[new_p_id]['input_device_info']['df_list'][0]['id'],project_set[new_p_id]['output_device_info']['df_list'][i]['id']];
        '''
        data = {'setting_info': json.dumps({'connect_info': connect_info, 'p_id': new_p_id})}
        response = post_to_ccm('/save_connection_line', data)
        project_set[new_p_id]['na_id_list'].append(response['na_id'])


def delete_project_handler(p_id, mac_addr):
    print('delete_project p_id=',p_id,' mac_addr=',mac_addr)
    data = {'p_id': p_id}
    deregister(mac_addr)
    response = post_to_ccm('/delete_project', data)
    if int(p_id) in project_set:
        del project_set[int(p_id)]

def deregister(mac_addr):
    print('deregister mac_addr ',mac_addr)
    r = requests.delete(config.iottalk_server + config.csm_path + '/' + mac_addr)
    if r.status_code != 200 and r.status_code != 400: raise CSMError(r.text)
    return True

def post_to_ccm(url, data):
    r = requests.post(config.iottalk_server + config.ccm_path + url, data=data)
    try:
        response = tornado.escape.json_decode(r.text)
    except:
        response = r.text
    return response
