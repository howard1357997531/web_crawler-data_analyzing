$(document).ready(function () {
    $(document).on('click','.std_btn', function () {
        const std_name = $('#std_name').val()
        console.log(std_name)
        $.ajax({
            url: "/get_grade",
            data: {
                'std_name':std_name
            },
            dataType: "json",
            beforeSend:function(){
				
			},
            success: function (res) {
                $('.std_chart').html(res.data)
                
            }
        });
    });

    $(document).on('click','.std_rank', function () {
        $.ajax({
            url: "/get_rank",
            data: {
                
            },
            dataType: "json",
            beforeSend:function(){
				
			},
            success: function (res) {
                $('#std_table').html(res.data)
                console.log(res.data)
            }
        });
    });

    $(document).on('click','.editbtn', function () {
        const st_id = $(this).data('id')
        console.log(st_id)
        $.ajax({
            url: "/edit_grade",
            data: {
                'st_id':st_id
            },
            dataType: "json",
            beforeSend:function(){
				
			},
            success: function (res) {
                $('.form-content').html(res.data)
            }
        });
    });
    
    $('.std_edit').submit(function (e) { 
        var s = $(this).serialize()
        //serialize 後的值
        //csrfmiddlewaretoken=rMLCG6AgHrPJNq8ieDRGj7bPx1woA2pExK7LK8spr4OrP1HcZUcKjy2NLQ7VWB5H&name=%E5%B0%8F%E5%B0%8F%E5%85%B5&
        //code=A10020022&sex=%E7%94%B7&chinese=57&english=78&math=88&society=68&science=48
        console.log(s)
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: "json",
            success: function (res) {
                console.log(res.bool)
                if (res.bool == true) {
                    $('.modal').modal('hide');
                    $('.datacon').load(location.href + ' .datacon');  //如果html有地方用js改過，
                    //location.reload();                                  //局部reload不會reload js
                }
                
            }
        });
        e.preventDefault();
        
    });
    
    $('.std_delete').submit(function (e) { 
        const s = $(this).serialize()
        const std_name = $(this).data('name')
        console.log(std_name)
        swal({
            title: "警告 !",
            text: `確定刪除 ${std_name} ?`,
            icon: "warning",
            buttons: true,
            dangerMode: true,
          })
          .then((willDelete) => {
            if (willDelete) {
                $.ajax({
                    type: $(this).attr('method'),
                    url: $(this).attr('action'),
                    data: $(this).serialize(),
                    dataType: "json",
                    success: function (res) {
                        console.log(res.bool)
                        if (res.bool == true) {
                            swal("資料已刪除 ~", {
                                icon: "success",
                              });
                            $('.datacon').load(location.href + ' .datacon');
                            //location.reload();
                        }
                        
                    }
                });
              
            } else {
              swal("您的資料未刪除 ~");
            }
          });
        
        e.preventDefault();
        
    });
    
});