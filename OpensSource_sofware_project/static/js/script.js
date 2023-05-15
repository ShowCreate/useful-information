function executeScript() {
    var loadingOverlay = document.getElementById("loading-overlay");
    loadingOverlay.style.display = "block";
  
    setTimeout(function() {
        var button = document.querySelector(".s-button");
        button.style.display = "none";
      
      // 스크립트 실행 후 10초 후에 다음 페이지로 이동
      setTimeout(function() {
        window.location.href = "/main";
      }, 10000);
    }, 0);
  }
  
