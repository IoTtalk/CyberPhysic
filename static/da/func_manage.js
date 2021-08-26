var func_def = "def run(*args):\n"; 

function create_function(f_name,func_content,idf_index,ido_id){
    var temp_fn_info = save_function_info(f_name,project_info.in_device[ido_id].idf_id_list[idf_index],0,func_content,0,1,"");
    var fnvt_idx = temp_fn_info.fnvt_idx;
    if(fnvt_idx != 0){
        //save temp function
        project_info.fn_id_list.push(save_a_temp_function(fnvt_idx).fn_id);
    }
}

function save_precession_func(){   
    var idf_index = 0;
    var response = check_function_exist("precession");
    if(response.is_exist != false){
        //function exists
        project_info.fn_id_list.push(response.is_exist[0]);  
    }else{
        //create temp function
        var func_content = func_def+
            "\ttmp = sum(i*i for i in args)**0.5\n"+
            "\tif tmp > 3:\n"+
            "\t\treturn abs (20 - tmp)\n"+
            "\telse:\n"+
            "\t\treturn 20";
        create_function("precession",func_content,idf_index,0);
    }
    get_proj_exception();
    save_connection_configuration(idf_index);
}
/*
//上下：Height 左右：Angle 前後：Speed
function save_tennis_func(){
    var idf_index = 0;
    var response = check_function_exist("tennis_angle");
    if(response.is_exist != false){
        //function exists
        console.log("function exist.");
        project_info.fn_id_list.push(response.is_exist[0]);  
    }else{
        //create temp function
        var func_content = func_def+
            tab+"tmp = abs(args[0])\n"+
            tab+"if tmp > 1 and tmp < 18:\n"+
            double_tab+"return tmp*10\n"+
            tab+"elif tmp < 1:\n"+
            double_tab+"return 0"+
            tab+"else:\n"+
            double_tab+"return 180";
        create_function("tennis_angle",func_content,idf_index);
    }

    response = check_function_exist("tennis_height");
    if(response.is_exist != false){
        //function exists
        console.log("function exist.");
        project_info.fn_id_list.push(response.is_exist[0]);  
    }else{
        //create temp function
        var func_content = func_def+
            tab+"if abs(args[2]) < 3 :\n"+
            double_tab+"return 0\n"+
            tab+"else:\n"+
            double_tab+"return 35+3*args[2]";
        create_function("tennis_height",func_content,idf_index);
    }

    response = check_function_exist("tennis_speed");
    if(response.is_exist != false){
        //function exists
        console.log("function exist.");
        project_info.fn_id_list.push(response.is_exist[0]);
    }else{
        //create temp function
        var func_content = func_def+
            tab+"tmp = abs(args[1])\n"+
            tab+"if tmp > 2:\n"+
            double_tab+"return tmp * 10\n"+
            tab+"else:\n"+
            double_tab+"return 0";
        //var func_content = "def run(*args):\n    tmp = abs(args[1])\n    if(tmp > 2):\n        return tmp*10\n    else:\n        return 0";
        create_function("tennis_speed",func_content,idf_index);
    }

    get_proj_exception();
    save_connection_configuration(idf_index);
}
*/

//前後:gravity 左右:speed
function save_universe_func(){
    var idf_index = 0;
    //function for odf gravity
    var response = check_function_exist("universe_gravity");
    if(response.is_exist != false){
        //function exists
        project_info.fn_id_list.push(response.is_exist[0]);  
    }else{
        //create temp function
        var func_content = func_def+
            "\tif args[1] == -1 :\n"+
            "\t\treturn -1\n"+
            "\telse:\n"+
            "\t\tif abs(args[1]) < 2:\n"+
            "\t\t\treturn 0\n"+
            "\t\telse:\n"+
            "\t\t\treturn abs(args[1])";
        create_function("universe_gravity",func_content,idf_index,0);
    }

    //function for odf speed
    var response = check_function_exist("universe_speed");
    if(response.is_exist != false){
        //function exists
        project_info.fn_id_list.push(response.is_exist[0]);  
    }else{
        //create temp function
        var func_content = func_def+
            "\tif args[0] == -1 :\n"+
            "\t\treturn -1\n"+
            "\telse:\n"+
            "\t\tif abs(args[0]) < 2:\n"+
            "\t\t\treturn 0\n"+
            "\t\telse:\n"+
            "\t\t\treturn abs(args[0])";
        create_function("universe_speed",func_content,idf_index,1);
    }
    get_proj_exception();
    save_connection_configuration(idf_index);
}

//手機朝左右：mass 手機朝上下：gravity
function save_snakepend_func(){
    var idf_index = 2;
    
    var response = check_function_exist("snake_gravity");
    if(response.is_exist != false){
        //function exists
        project_info.fn_id_list.push(response.is_exist[0]);  
    }else{
        //create temp function
        var func_content = func_def+
            "\tif abs(args[1]) < 5:\n"+
            "\t\treturn 0\n"+
            "\telse:\n"+
            "\t\treturn args[1]";
        create_function("snake_gravity",func_content,idf_index,0);
    }

    response = check_function_exist("snake_mass");
    if(response.is_exist != false){
        //function exists
        project_info.fn_id_list.push(response.is_exist[0]);  
    }else{
        //create temp function
        var func_content = func_def+
            "\ttmp = abs(args[0])\n"+
            "\tif tmp > 200:\n"+
            "\t\tif args[0] > 0:\n"+
            "\t\t\treturn 360-tmp\n"+
            "\t\telse:\n"+
            "\t\t\treturn tmp - 360\n"+
            "\telif tmp < 2:\n"+
            "\t\treturn 0\n"+
            "\telse:\n"+
            "\t\treturn -args[0]";
        create_function("snake_mass",func_content,idf_index,1);
    }

    get_proj_exception();
    save_connection_configuration(idf_index);
}

function check_function_exist(f_name){
    var data = {'function_name':f_name};
    var response = my_ajax('/csm/QRpage/check_function_exist',data);   
    return response;
}

function save_connection_configuration(idf_index){
    for(var i = 0; i < project_info.output_device_info.df_list.length; i++){
        var info = {
            'join_name':'Join '+(i+1).toString(),
            'na_id':project_info.na_id_list[i],
            'all_idfo_id':[project_info.in_device[i].idf_id_list[idf_index]],
            'all_idf_info':[["variant","variant","variant"]],
            'all_idf_fn_id':[project_info.fn_id_list[i]],
            'odfo_id': project_info.output_device_info.df_list[i].id,
            'odf_info': ['-1'],
            'join_index':[],
        };
        var function_setting = {'setting_list':info,'p_id':project_info.p_id};
        var data = {'function_setting':function_setting};
        my_ajax('/ccm/save_connection_configuration',data);
    }   
}

function save_function_info(func_name, df_id, fnvt_idx, func_content, is_switch, ver_enable, non_df_argument){
    var fn_info = {
        'fn_name':func_name,
        'fnvt_idx':fnvt_idx, 
        'code':func_content,
        'df_id':df_id, 
        'is_switch':is_switch, 
        'ver_enable':ver_enable, 
        'non_df_argument':non_df_argument 
    }
    var data = {'fn_info':fn_info};
    var response = my_ajax('/ccm/save_function_info',data);
    console.log("save function info res:",response);
    return response;
}

function save_a_temp_function(fnvt_idx){
    var data = {'fnvt_idx':fnvt_idx};
    var response = my_ajax('/ccm/save_a_temp_function',data);
    return response;
}
