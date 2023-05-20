function executeScript() {
    var loadingOverlay = document.getElementById("loading-overlay");
    loadingOverlay.style.display = "block";
  
    setTimeout(function() {
        var button = document.querySelector(".s-button");
        button.style.display = "none";
      
      //여기에 정보를 크로울링 하는 \

        // 파이썬 파일 실행 요청을 서버로 전송
  fetch('/execute_python_script')
    .then(response => {
      if (response.ok) {
        console.log('파이썬 파일 실행 요청이 성공적으로 전송되었습니다.');
        window.location.href = '/main';
      } else {
        console.log('파이썬 파일 실행 요청이 실패하였습니다.');
      }
    })
    .catch(error => {
      console.error('오류 발생:', error);
    });
  }, );
  }
  
