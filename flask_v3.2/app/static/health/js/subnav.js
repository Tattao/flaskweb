

    $(function(){
        
        $.ajax({
            url: 'tpls/subnav.html',
            dataType: 'html',
            async: false,
            success: function(data){
                $('.mc-subNav').html(data);
            }
        })

        $.ajax({
            url: 'tpls/header.html',
            dataType: 'html',
            async: false,
            success: function(data){
                $('#header').html(data);
            }
        })
            
        var $subNav = $('.mc-subNav');
        $('.logoBtn').on('click', function(){
            if($subNav.width()){                   
                $subNav.find('.panel-group').fadeOut();
                $subNav.addClass('subNavHide');
                $('.content').addClass('move');
                $('footer').addClass('move');
            }
            else{
                $subNav.removeClass('subNavHide');
                $subNav.find('.panel-group').show(700);
                $('.content').removeClass('move');
                $('footer').removeClass('move');
            }
            
        })
    })

    