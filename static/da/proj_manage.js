$(window).on("load",function(){
    check_device_registered();
    turn_on_project();
    create_QRcode();
});

$(window).bind('beforeunload',function(){
    /*
        Send request to cyberphysic server, then server delete project related info and deregister for this da.
        Didn't deregister here because of time limit(There is just enough time for one request).
    */
    delete_project();
});

function check_device_registered(){
    console.log('d_name:',d_name);
    if(d_name != null){
        query_d_id(d_name, function(response){
            bind_device(odo_id, d_name, response, function(response){
                get_proj_exception();
            });
        });
    }else{
        setTimeout(check_device_registered, 100);
    }
}

function turn_on_project(){
    var form_data = new FormData();
    form_data.append('p_id', p_id);

    my_ajax(iottalk_server, ccm_path, '/turn_on_project', form_data);
}

function create_QRcode(){
    let url = cyberphysic_server + "/rc/"+ str(p_id);
    $('#qrcode').qrcode({
      width: 250,
      height: 250,
      text: url});

    $('#hidden_link').on('click',function(){
        window.open(url);
    });
}

function get_proj_exception(){
    var form_data = new FormData();
    form_data.append('p_id', p_id);

    my_ajax(iottalk_server, ccm_path, '/get_exception_status', form_data, function(response){
        console.log("get_exception_status:",response);
        if(response.redraw == true){
            setTimeout(get_proj_exception,100);
        }  
    });
}

function delete_project(){
    var url = cyberphysic_server + '/delete_project/' + p_id + '/' + device_mac_addr;
    superagent
        .delete(url)
        .set('Accept', 'application/json')
        .then(res => {
            console.log(url, ' success, response=', res)
        })
        .catch(err => {
            console.log(url, ' error, e= ',err);// err.message, err.response
        });
}

// function delete_project(){
//     $.ajax({
//         url: cyberphysic_server+ '/delete_project/' + p_id + '/' + device_mac_addr,
//         type: 'DELETE',
//         cache: false,
//         dataType: 'json',
//         error:function(e){
//             console.log(url, ' error, e= ',e);
//         },
//         success:function(response){
//             console.log(url, ' success, response=', response);
//         },
//     });
// }