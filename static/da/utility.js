function my_ajax(ip, path, url, data, success_callback){
    success_callback = (typeof success_callback != 'undefined') ? success_callback : null;
    $.ajax({
        url: ip + path + url,
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        dataType: 'json',
        error:function(e){
            if(e.status != 404 && success_callback){
                success_callback(e);
            }else{
                console.log(url, ' error, e= ',e);
            }
        },
        success:function(response){
            if(success_callback){
                success_callback(response);
            }else{
                console.log(url, ' success, response=', response);
            }
        },     
    });
}

//用d_name來query d_id
function query_d_id(d_name, callback){
    var form_data = new FormData();
    form_data.append('d_name', d_name);

    my_ajax(iottalk_server, ccm_path, '/get_d_id_from_d_name', form_data, callback);
}   

//bind device
function bind_device(odo_id,d_name, d_id, callback){
    callback = (typeof callback != 'undefined') ? callback : null;
    var device_save_info = [ odo_id, d_name, d_id];
    var form_data = new FormData();
    form_data.append('device_save_info', JSON.stringify(device_save_info));

    console.log("bind_device: ",device_save_info);
    my_ajax(iottalk_server, ccm_path, '/bind_device', form_data, callback);
}