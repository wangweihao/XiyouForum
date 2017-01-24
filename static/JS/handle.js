/**
 * Created by wwh on 2016/11/29.
 */

host = 'http://127.0.0.1:8080';
SUCCESS = 0;
DB_ERR_DUP_EML = 1;
DB_ERR_DUP_NAM = 2;
DB_ERR_HAND = 3;
JSON_ERR_ANALY = 4;

count = 0;

function loginCallback() {
    $('#email_tag').addClass('hidden');
    var email   = $('#login-email').val();
    var passwd  = $('#login-passwd').val();
    email_pattern = /^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/;


    if (email == '') {
        $('#email_tag').removeClass('hidden');
        return;
    }else if (email_pattern.test(email) == false){
        $('#email_tag').removeClass('hidden');
        $('#email_tag').text('邮箱格式错误');
        return;
    }else if (passwd == '') {
        $('#passwd_tag').text('请输入密码');
        $('#passwd_tag').css('color', 'red');
        return;
    }else if (passwd.length < 6 || passwd.length > 20) {
        $('#passwd_tag').text('密码长度错误');
        $('#passwd_tag').css('color', 'red');
        return;
    }

    var request = {
        email : email,
        passwd: passwd
    };

    $.ajax({
        type : 'POST',
        url  : host + '/api/user/login',
        data :  JSON.stringify(request),
        dataType:'json',
        async:  true,
        success : function (data) {
            if(data.status == 'ok') {
                alert('登录成功...正在跳转');
                // $("body").removeClass("modal-open");
                // $('#login-out').addClass('hidden');
                // $('#login-in').removeClass('hidden');
                // $('#u-nickname').text(data.data['nickname']);
                // $('#head_url').attr("src", data.data['head_url']);
                location.reload()
                // document.cookie = 'id=' + data.data['id'];
                // document.cookie = 'nickname=' + data.data['nickname'];
            }else if(data.status == 'error'){
                alert('登录失败:'+data.info);
            }

        },
        error:function () {
            alert("系统繁忙，请稍后再试");
        }
    });
}

function registerCallback() {
    $('#reg_nickname-tag').addClass('hidden');
    $('#reg-email_tag').addClass('hidden');
    $('#reg-passwd_tag').addClass('hidden');
    $('#reg-repasswd_tag').addClass('hidden');

    var nickname  = $('#nickname').val();
    var email     = $('#reg-email').val();
    var passwd    = $('#reg-passwd').val();
    var re_passwd = $('#reg-repasswd').val();
    email_pattern = /^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/;

    if (nickname == ''){
        $('#reg-nickname_tag').removeClass('hidden');
        return;
    }else if (email == '') {
        $('#reg-email_tag').removeClass('hidden');
        return;
    }else if (email_pattern.test(email) == false){
        $('#reg-email_tag').removeClass('hidden');
        $('#reg-email_tag').text('邮箱格式错误');
        return;
    }else if (passwd == '') {
        $('#reg-passwd_tag').removeClass('hidden');
        return;
    }else if (re_passwd == '') {
        $('#reg-repasswd_tag').removeClass('hidden');
        return;
    }

    if (passwd.length < 6 || passwd.length > 20) {
        $('#reg-passwd_tag').removeClass('hidden');
        $('#reg-passwd_tag').text('密码长度不正确');
        return;
    }
    if (passwd != re_passwd) {
        $('#reg-repasswd_tag').removeClass('hidden');
        $('#reg-repasswd_tag').text('两次输入密码不一致');
        return;
    }

    var request = {
        nickname : nickname,
        email    : email,
        passwd   : passwd
    };

    $.ajax({
        type  : 'POST',
        url   : host + '/api/user/register',
        data : JSON.stringify(request),
        dataType:'json',
        async: true,
        success : function (data) {
            if (data.status == 'ok') {
                alert('恭喜你注册成功');
                $('#reg-close').click();
                $('#nav-login-btn').click();
            }else if(data.status == 'error'){
                alert(data.type);
                switch (data.type){
                    case DB_ERR_DUP_NAM:{
                        $('#reg-nickname_tag').removeClass('hidden');
                        $('#reg-nickname_tag').text(data.info);
                        break;
                    }
                    case DB_ERR_DUP_EML:{
                        $('#reg-email_tag').removeClass('hidden');
                        $('#reg-email_tag').text(data.info);
                        break;
                    }
                }
            }
            return;
        },
        error:function (data) {
            alert('注册失败：系统错误，请稍后再试..');
        }
    });
}

function quitLogin() {
    $.ajax({
        type : 'POST',
        url  : host + '/api/user/quit',
        async: true,
        success:function () {
            $('#login-in').addClass('hidden');
            $('#login-out').removeClass('hidden');
            alert('退出成功');
        },
        error:function () {
            alert('退出失败');
        }
    });
    // $('#login-in').addClass('hidden');
    // $('#login-out').removeClass('hidden');
    //
    // delete_cookie('nickname');
    // delete_cookie('session_id');
}

function switchNewestTab() {
    $('#que-newest').addClass('active');
    $('#que-hottest').removeClass('active');
    $('#que-unanswer').removeClass('active');
}

function switchHottestTab() {
    $('#que-newest').removeClass('active');
    $('#que-hottest').addClass('active');
    $('#que-unanswer').removeClass('active');
}

function switchUnanswerTab() {
    $('#que-newest').removeClass('active');
    $('#que-unanswer').addClass('active');
    $('#que-hottest').removeClass('active');
}

function delete_cookie( name ) {
  document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function scan_time_inc() {

}

function getCookie(name)
{
    var arr, reg= new RegExp("(^| )"+name+"=([^;]*)(;|$)");

    if(arr=document.cookie.match(reg))

        return unescape(arr[2]);
    else
        return null;
}

function editSelfInfo() {
    if(count == 0) {
        $('.change').removeClass('hidden');
        $('#change-head').removeClass('hidden');
        $('#btn-self-info').text('完成资料修改');
        count = 1;
    }else if(count == 1) {
        $('.change').addClass('hidden');
        $('#change-head').addClass('hidden');
        $('#btn-self-info').text('编辑个人资料');
        count = 0;
    }
}

function changeSelfIntro() {
    $('#self-intro').removeClass('hidden');
}

function deterChangeSelfIntro() {
    var info = $("#self-intro input[type='text']").val();

    request = {
        userinfo : 'aWordIntro',
        content  : info
    };

    $.ajax({
        type : 'POST',
        url  : host + '/update/userinfo',
        data :  JSON.stringify(request),
        dataType:'json',
        async:  true,
        success : function (data) {
            if(data.status == 'ok') {
                alert('修改成功...');
                $('#self-intro').addClass('hidden');
                $('#sp-self-intro').html(info);
            }else if(data.status == 'error'){
                alert('修改失败:'+data.info);
            }

        },
        error:function () {
            alert("系统繁忙，请稍后再试");
        }
    });
}

function cancelChangeSelfIntro() {
    $('#self-intro').addClass('hidden');
}

function changeSex() {
    $('#sex').removeClass('hidden');
}

function deterChangeSex() {
    var info = $("#sex input:radio:checked").val();

    request = {
        userinfo : 'sex',
        content  :  info
    };

    $.ajax({
        type : 'POST',
        url  : host + '/update/userinfo',
        data :  JSON.stringify(request),
        dataType:'json',
        async:  true,
        success : function (data) {
            if(data.status == 'ok') {
                alert('修改成功...');
                $('#sex').addClass('hidden');
                $('#sp-sex').html((info==0?'男':'女'));
            }else if(data.status == 'error'){
                alert('修改失败:'+data.info);
            }

        },
        error:function () {
            alert("系统繁忙，请稍后再试");
        }
    });
}

function cancelChangeSex() {
    $('#sex').addClass('hidden');
}

function changeSchool() {
    $('#school').removeClass('hidden');
}

function deterChangeSchool() {
    var info = $("#school input[type='text']").val();

    request = {
        userinfo : 'school',
        content  : info
    };

    $.ajax({
        type : 'POST',
        url  : host + '/update/userinfo',
        data :  JSON.stringify(request),
        dataType:'json',
        async:  true,
        success : function (data) {
            if(data.status == 'ok') {
                alert('修改成功...');
                $('#school').addClass('hidden');
                $('#sp-school').html(info);
            }else if(data.status == 'error'){
                alert('修改失败:'+data.info);
            }

        },
        error:function () {
            alert("系统繁忙，请稍后再试");
        }
    });
}

function cancelChangeSchool() {
    $('#school').addClass('hidden');
}

function changeSpecialty() {
    $('#specialty').removeClass('hidden');
}

function deterChangeSpecialty() {
    var info = $("#specialty input[type='text']").val();

    request = {
        userinfo : 'specialty',
        content  : info
    };

    $.ajax({
        type : 'POST',
        url  : host + '/update/userinfo',
        data :  JSON.stringify(request),
        dataType:'json',
        async:  true,
        success : function (data) {
            if(data.status == 'ok') {
                alert('修改成功...');
                $('#specialty').addClass('hidden');
                $('#sp-specialty').html(info);
            }else if(data.status == 'error'){
                alert('修改失败:'+data.info);
            }

        },
        error:function () {
            alert("系统繁忙，请稍后再试");
        }
    });
}

function cancelChangeSpecialty() {
    $('#specialty').addClass('hidden');
}

function changeAddress() {
    $('#address').removeClass('hidden');
}

function deterChangeAddress() {
    var info = $("#address input[type='text']").val();

    request = {
        userinfo : 'address',
        content  : info
    };

    $.ajax({
        type : 'POST',
        url  : host + '/update/userinfo',
        data :  JSON.stringify(request),
        dataType:'json',
        async:  true,
        success : function (data) {
            if(data.status == 'ok') {
                alert('修改成功...');
                $('#address').addClass('hidden');
                $('#sp-address').html(info);
            }else if(data.status == 'error'){
                alert('修改失败:'+data.info);
            }

        },
        error:function () {
            alert("系统繁忙，请稍后再试");
        }
    });
}

function cancelChangeAddress() {
    $('#address').addClass('hidden');
}

function changeQQ(){
    $('#qq').removeClass('hidden');
}

function deterChangeQQ() {
    var info = $("#qq input[type='text']").val();

    request = {
        userinfo : 'qq',
        content  : info
    };

    $.ajax({
        type : 'POST',
        url  : host + '/update/userinfo',
        data :  JSON.stringify(request),
        dataType:'json',
        async:  true,
        success : function (data) {
            if(data.status == 'ok') {
                alert('修改成功...');
                $('#qq').addClass('hidden');
                $('#sp-qq').html(info);
            }else if(data.status == 'error'){
                alert('修改失败:'+data.info);
            }

        },
        error:function () {
            alert("系统繁忙，请稍后再试");
        }
    });
}

function cancelChangeQQ() {
    $('#qq').addClass('hidden');
}

function changeWechat(){
    $('#wechat').removeClass('hidden');
}

function deterChangeWechat() {
    var info = $("#wechat input[type='text']").val();

    request = {
        userinfo : 'wechat',
        content  : info
    };

    $.ajax({
        type : 'POST',
        url  : host + '/update/userinfo',
        data :  JSON.stringify(request),
        dataType:'json',
        async:  true,
        success : function (data) {
            if(data.status == 'ok') {
                alert('修改成功...');
                $('#wechat').addClass('hidden');
                $('#sp-wechat').html(info);
            }else if(data.status == 'error'){
                alert('修改失败:'+data.info);
            }

        },
        error:function () {
            alert("系统繁忙，请稍后再试");
        }
    });
}

function cancelChangeWechat() {
    $('#wechat').addClass('hidden');
}

function changeEmail() {
    $('#email').removeClass('hidden');
}

function deterChangeEmail() {
    var info = $("#email input[type='text']").val();

    request = {
        userinfo : 'email',
        content  : info
    };

    $.ajax({
        type : 'POST',
        url  : host + '/update/userinfo',
        data :  JSON.stringify(request),
        dataType:'json',
        async:  true,
        success : function (data) {
            if(data.status == 'ok') {
                alert('修改成功...');
                $('#email').addClass('hidden');
                $('#sp-email').html(info);
            }else if(data.status == 'error'){
                alert('修改失败:'+data.info);
            }
        },
        error:function () {
            alert("系统繁忙，请稍后再试");
        }
    });
}

function cancelChangeEmail() {
    $('#email').addClass('hidden');
}

function changeSelfInfo() {
    $('#self-info').removeClass('hidden');
}

function deterChangeSelfInfo() {
    var info = $("#self-info input[type='text']").val();

    request = {
        userinfo : 'selfIntro',
        content  : info
    };

    $.ajax({
        type : 'POST',
        url  : host + '/update/userinfo',
        data :  JSON.stringify(request),
        dataType:'json',
        async:  true,
        success : function (data) {
            if(data.status == 'ok') {
                alert('修改成功...');
                $('#self-info').addClass('hidden');
                $('#sp-self-info').html(info);
            }else if(data.status == 'error'){
                alert('修改失败:'+data.info);
            }
        },
        error:function () {
            alert("系统繁忙，请稍后再试");
        }
    });
}

function cancelChangeSelfInfo() {
    $('#self-info').addClass('hidden');
}

function changeHead() {
    $('#change-head').click();
}

// function uploadHead() {
//     alert('点击更换');
//     $('#upload-head').click();
// }

$('#btn-agree').click(function(event) {
    event.preventDefault();
    var data = $(this).attr('data-id');
    var request = {
        qid  : data
    };
    alert(request);
    $.ajax({
        type:'POST',
        url : host + '/api/user/agree_ques',
        data: JSON.stringify(request),
        dataType: 'json',
        async:true,
        success: function () {
            alert("点赞");
        },
        error:function () {
            alert("点赞失败");
        }
    })
});
$('#btn-oppose').click(function(event) {
    event.preventDefault();
    data = $(this).attr('data-id');
    alert(data)
});
$('.btn-answ-agree').click(function(event) {
    event.preventDefault();
    data = $(this).attr('data-id');
    alert(data)
});
$('.btn-answ-oppose').click(function(event) {
    event.preventDefault();
    data = $(this).attr('data-id');
    alert(data)
});

$('form').submit(function (event) {
      event.preventDefault();
      var form = $(this);

      if (!form.hasClass('fupload')) {
        //普通表单
        $.ajax({
          type: "POST",
          url: form.attr('action'),
          data: form.serialize()
        }).success(function () {
          //成功提交
        }).fail(function (jqXHR, textStatus, errorThrown) {
          //错误信息
        });
      }
      else {
          //mulitipart form,如文件上传类
          var formData = new FormData(this);
          $.ajax({
              type: "POST",
              url: form.attr('action'),
              data: formData,
              dataType: "json",
              mimeType: "multipart/form-data",
              contentType: false,
              cache: false,
              processData: false
          }).success(function (data) {
              //成功提交
              $("#myHead").attr('src',data['url']);
          }).fail(function (jqXHR, textStatus, errorThrown) {
              //错误信息
          });
      };
    });
