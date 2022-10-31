   var WatchList = document.getElementsByClassName('ri-add-line');

   //for each one of the WatchList elements add a event listener when its clicked
   for(var i = 0; i < WatchList.length; i++){
      WatchList[i].addEventListener('click', function(e){
         e.preventDefault();
         var project = this.getAttribute('value');
         var url = '';
         var data = {
            'project': project
         };
         $.ajax({
            headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': '{{ csrf_token }}',
            },
            url: url,
            type: 'POST',
            data: JSON.stringify(data),
         });
      //then replace the inner content with a check mark
      this.innerHTML = '<i class="ri-check-line"></i>';
      //then change the class to nothing
      this.className = '';
      });
   }
