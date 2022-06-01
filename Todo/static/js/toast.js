
toastIcons = {
    success: 'fa-solid fa-circle-check',
    error: 'fa-solid fa-triangle-exclamation',
    alert: 'fa-solid fa-circle-exclamation'
}

function toast(options = {
    containerSelector: '#toast',
    title: '',
    body: '',
    type: '',
    duration: 4000
}) {
    const toast = document.querySelector(options.containerSelector)
    if (!toast){
        return
    }
    const toastMessage = document.createElement('div')
    toastMessage.classList.add('toast__item')
    toastMessage.innerHTML = `
    <div class="toast__icon"><i class="${toastIcons[options.type]}"></i></div>
    <div class="toast__message">
        <h3 class="toast__title">${options.title}</h3>
        <p class="toast__body">${options.body}</p>
    </div>
    <div class="toast__close"><i class="fa-regular fa-circle-xmark"></i></div>
    `
    toast.appendChild(toastMessage)
    // for animation
    setTimeout(()=>{
        toastMessage.classList.add(options.type)
    },100)

    var autoDelete = setTimeout(() => {
       removeToast(toastMessage) 
    }, options.duration);


    // add close event 
    const closeBtn = toastMessage.querySelector('.toast__close')
    closeBtn.onclick = ()=>{
        clearTimeout(autoDelete)
        removeToast(toastMessage)
    }

    function removeToast(toastMessage) {
        setTimeout(()=>{
            toastMessage.remove()
        }, 400)
        toastMessage.classList.remove(options.type)
    }
}

function formReplace(options = {
    formSelector: '#login-form',
    type: 'success',
    title: 'sucessfully',
    body: '',
    link: '#',
    linkName:'Login'
}) {
    var form = document.querySelector(options.formSelector)
    var container  = form.parentNode
    var toReplace = document.createElement('div')
    form.remove()

    toReplace.classList.add('form-replace', options.type)
    toReplace.innerHTML = `
        <div class="replace-form">
            <div class="replace__icon"><i class="${toastIcons[options.type]}"></i></div>
            <div class="replace__message">
               <h3 class="replace__title">${options.title}</h3>
                <p class="replace__body">${options.body}</p>
            </div>
            <a class="replace__link" href="${options.link}">${options.linkName}</a>
        </div>
    `
    container.append(toReplace)
}