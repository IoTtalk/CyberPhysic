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

    my_ajax(iottalk_ip, ccm_port, '/turn_on_project', form_data);
}

function create_QRcode(){
    let url = cyberphysic_server_ip + ":"+ cyberphysic_server_port + "/rc/"+ str(p_id);
    let QRcode_url = "https://chart.googleapis.com/"
                +"chart?chs=250x250&cht=qr&choe=UTF-8&chl="
                + url;
    $('#qrcode').attr('src',QRcode_url);
    $('#hidden_link').on('click',function(){
        window.open(url);
    });
}

function get_proj_exception(){
    var form_data = new FormData();
    form_data.append('p_id', p_id);

    my_ajax(iottalk_ip, ccm_port, '/get_exception_status', form_data, function(response){
        console.log("get_exception_status:",response);
        if(response.redraw == true){
            setTimeout(get_proj_exception,100);
        }  
    });
}

function delete_project(){
    $.ajax({
        url: cyberphysic_server_ip + ":" + cyberphysic_server_port + '/delete_project/' + p_id + '/' + device_mac_addr,
        type: 'DELETE',
        cache: false,
        dataType: 'json',
        error:function(e){
            console.log(url, ' error, e= ',e);
        },
        success:function(response){
            console.log(url, ' success, response=', response);
        },
    });
}