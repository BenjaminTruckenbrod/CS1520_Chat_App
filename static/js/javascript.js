function setup(){
    addListeners();
}
function addListeners(){
    // let reg = document.getElementById("register");
    // reg.addEventListener("click", validateForm)
}

function validateForm() {
    let password1 = document.forms["registration"]["password"].value;
    let password2 = document.forms["registration"]["password2"].value;

    if (password1 == ''){
        alert ("Please enter Password");
        return false;
    }
      
    else if (password2 == ''){
        alert ("Please enter confirm password");
        return false
    }


    else ([password1==password2])
        return true
}


window.addEventListener('load', setup);

// addListeners();
