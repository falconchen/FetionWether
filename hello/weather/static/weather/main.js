$(document).ready(
    function () {
         //不知道为什么会有两个空的 li , 删除它们
        $('#forecast li').each(
            function() {
                if ($(this).attr('class') != 'cast') {
                    $(this).remove()
                }
            }
        );

        //高亮当前action
        var action = $('input[name=action]').val() ;
        if  (action == undefined) {
            $('a#insert').addClass('highlight');
        }else {
            $('a#'+action).addClass('highlight')
        }



         $.getScript('http://61.4.185.48:81/g/');

        //生成二级联动列表
        if(document.getElementById('province') != null) {
	        get_provinces() ;               
	        
                //http://m.weather.com.cn/data/101010100.html
         //$.getScript('http://61.4.185.48:81/g/');
            
            
	         //返回内容如 ： var ip="121.35.167.179";var id=101280601;if(typeof(id_callback)!="undefined"){id_callback();}        
	        $('input#subtype_1').click(function(){alert('说明:\n预报内容将由发送时间决定\n0~12时是为当日下雨的预报;\n13~23时为次日下雨的预报。\n没有收到短信表示预报不会下雨\n推荐早上起床或出门前（如7/8点）接收以决定是否带雨具')});
	        
        }
        
        //获取验证码
        $('#get_code').click(
	        	function(){
	        		phone_num = $('#phone_num').val();
	        		var reg = /^\d{11}$/;
	        		//console.log(reg.exec(phone_num))
	        		if (reg.exec(phone_num) == null)
	        			alert(phone_num + '不是有效的中国手机号码');
					else {
						//ajax
						//setTimeout(function(){alert('验证码已发送到你的手机')},3000)
						$.ajax({
						   type: "GET",
						   cache:false,
						   url: $('#get_code').attr('href'),
						   data: "phone_num="+phone_num,
						   success: function(msg){
						     alert( msg );
						     $('#get_code').text('重新获取验证码')
						   }
						});
						
					}	        			
	        		return false;
	        	}
	        );
        
        var is_valid = false;
        $('form#verify').submit(
        	function() {
        		if (is_valid == true) return true;
        		
        		var phone_num = $('#phone_num').val();
	        	var reg = /^\d{11}$/;
	        		//console.log(reg.exec(phone_num))
	        	if (reg.exec(phone_num) == null){
	        		alert(phone_num + '不是有效的手机号码');
	        		return false;
	        	}
				
				var code = $('#code').val();
				var reg = /^[A-Za-z0-9]{6}$/;
        		if (reg.exec(code) == null){
	        		alert('无效验证码');
	        		return false;
	        	}
        		
        		$.ajax({
        			type:"GET",
        			cache:false,
        			url:'../get_user_info/',
        			data:{'phone_num':phone_num,'code':code},
        			success: function(msg) {
        				var next_title = $('input[name=action]').attr('title'); 
        				if (window.confirm(msg+'确实要'+ next_title +'吗?')){
        					is_valid = true;
        					$('form#verify').submit();
        				}
        			},
        			complete: function(XMLHttpRequest, status){
        				if (status == 'error')
        					alert('验证码错误或超时，请重试')
                                        else 
                                        	alert('服务器繁忙，请稍后重试');
        			}	
        		})
        		
        		return false; 
        		
        	}
        )
        
    }

);

//加载天气信息脚本，并加信息渲染到当前页
function get_weather(id) {
    if("undefined" != typeof id) {
      var dataUrl = "http://falcon.sinaapp.com/weather/wt_jsonp.php?id=" + id ;
      jQuery.getJSON(dataUrl+"&callback=?", 
      function(data) {
          //console.log(data);
          //console.log(get_today_cn() )
          var info = data.weatherinfo;
          //alert(info.city+'（'+info.date_y+'):'+info.weather1+','+info.temp1);
          //alert(info.city+':'+info.weather1+info.temp1);
          if (get_today_cn() == info.date_y) {
                var today_cast=info.weather1 +"&nbsp;" + info.temp1 +"&nbsp;" +info.fx1 +info.fl1 
                var tomorrow_cast = info.weather2 +"&nbsp;" + info.temp2 
          }else {
                var today_cast=info.weather2 +"&nbsp;" + info.temp2 +"&nbsp;" +info.fx2 +info.fl1
                var tomorrow_cast =  info.weather3 +"&nbsp;" + info.temp3 
          }
        $('#location').html(info.city +':');
        $('#today_cast').html('今天: ' + today_cast +';');
        $('#tomorrow_cast').html('明天: ' + tomorrow_cast+'.');  
        if (ip !="undefined") {$('#ip_address').html('<b>您的IP:</b> ' + ip.replace(/_/g,''));}
        $('#forecast ul').fadeIn();
      });
    }
}

function get_today_cn() {
  var d = new Date()
  var vYear = d.getFullYear()
  var vMon = d.getMonth() + 1
  var vDay = d.getDate()
  return vYear +"年" +vMon +"月" +vDay+"日";
}

function id_callback() {

    
    id = get_main_city(id);
    //调用取天气数据的函数
    get_weather(id);
    
   // $.getScript('http://61.4.185.48:81/g/' ) {
    
    //}
         
                
    
    //根据该id取省份/城市下拉列表的值
    var area = get_area_obj(id);       
    //console.log(area);
    //var area = {'p':'广东','c':'深圳'};
    
    
    var obj = document.getElementById('province');
    if (obj == null) return ;
    for (i=0;i<obj.options.length;i++) {
        //console.log(obj.options[i].value);
        //确定选中的省份
        if (area['p'] == obj.options[i].value ) {
            obj.options[i].selected = true;
            on_pro_select_change('province');//确定下拉的城市列表
            
            //确定选中的城市 
            var city_obj = document.getElementById('city');
            for (i=0;i<city_obj.options.length;i++) {
                if (area['c'] == city_obj.options[i].text ) {
                    city_obj.options[i].selected = true;
                }
            }
            
        }
    }
    
    
}

//根据城市代码取地区信息,返回一个json对象
function get_area_obj(id) {
    for (prov in jdata) {
        var area = jdata[prov];
        for (code in area) {
            if (code == id) {
                return {'p':prov,'c':area[code],'id':id}
            }
        }
    }
    return {'p':'直辖市','c':'北京','id':101010100}
}


//取一级城市

function get_main_city(id){
    var ex_group = [101281802,101281402]; //例外的城市,如阳春，罗定    
    for (code in ex_group) {
        if (ex_group[code] == id) {
            id = id.toString();
            return id;
        }
    }
        
    if (id>=101010100 && id<101050100) { //直辖区内
        id = id.toString();
        id = id.substr(0,5) +'0100';            
    } else if(id>101050100 &&  id<101340904) { //各省一级城市
        id = id.toString();
        id = id.substr(0,7) + '01';        
    }else { //国外城市或未能探测到,取北京的作为默认
        id = '101010100'
    }
        
    return id;
}


//--------------------------------------------------------------------------------------
function on_pro_select_change(id) {

        var obj = document.getElementById(id);
        var index = obj.selectedIndex;         
        var se_prov = obj.options[index].value;
        //console.log(se_prov)        
        //省份一旦修改，下属城市也应该开始修改                
        var city_obj = document.getElementById('city');
        //清空原有城市列表
        city_obj.options.length = 0        
        //增加城市可选项
        var city_data = get_cities_under(se_prov);        
        var o = new Option('--请选择--',0);
         city_obj.options.add(o);
         
        for (city in city_data) {        
            var o = new Option(city_data[city],city);
            city_obj.options.add(o);
         }

}    

//城市改变时的钩子
function on_city_change(id) {
    return true;
}


//取省份列表
function get_provinces() {
     var prov_obj =document.getElementById('province');
     if (prov_obj == null) return ;
     prov_obj.length = 0;
    var o = new Option('--请选择--',0);
    prov_obj.options.add(o);
     for (prov in  jdata) {
        var o = new Option(prov,prov);        
        prov_obj.options.add(o);
     }
}
    
//按省份名取下属的城市列表    
function get_cities_under(province) {
    if(jdata[province] !=undefined) {
       return jdata[province];
    }else {       
       var invalid_city = {"-1": "无效城市"};
      return invalid_city;
    }
   
}
