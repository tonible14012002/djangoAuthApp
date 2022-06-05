function validator (options) {
    const form = document.querySelector(options.formSelector)

    if (form){
        // initialize status for each input element
        var rules = {}
        options.ruleOptions.forEach((rule)=>{
            // save rules
            if (rules.hasOwnProperty(rule.selector)) {
                rules[rule.selector].push(rule.test)
            }
            else {
                rules[rule.selector] = [rule.test]
            }

            var inputElement = document.querySelector(rule.selector)
            if (inputElement){
                var errorElement = inputElement.parentNode.querySelector(options.errorSelector)
                inputElement.onblur = () => {
                    var isValid = validator.validate(inputElement, rules[rule.selector], errorElement, options.errorClass) 
                }
                    
                inputElement.oninput = () => {
                    errorElement.innerHTML = ''
                    inputElement.parentNode.classList.remove(options.errorClass)
                }
            }                
        })      

        form.onsubmit = function (e) {
            e.preventDefault()
            var isFormValid = true
            //  validate all input
            options.ruleOptions.forEach((rule) => {
                var inputElement = document.querySelector(rule.selector)
                if (inputElement){
                    var errorElement = inputElement.parentNode.querySelector(options.errorSelector)
                    if (!validator.validate(inputElement, rules[rule.selector], errorElement, options.errorClass)){
                        isFormValid = false
                    }
                }       
            })

            if (isFormValid) {
                if (typeof options.onSubmit === 'function'){
                    var formData = new FormData(form)
                    var data = {}
                    formData.forEach((value, key) => {
                        data[key] = value
                    })
                    options.onSubmit(data)
                }
                else {
                    form.submit()
                }
            }
        }

    }
}

validator.validate = function (inputElement, tests, errorElement, errorClass) {
    for (var i in tests) {
        var errorMessage = tests[i](inputElement.value)
        if (errorMessage){
            errorElement.innerHTML = errorMessage  
            inputElement.parentNode.classList.add(errorClass)
            return false
        }
        else {
            errorElement.innerHTML = ''
            inputElement.parentNode.classList.remove(errorClass)
        }
    }
    return true
}

// rule generator
validator.isRequired = (selector, message)=>{
    return {
        selector: selector,
        test: (value) => {
            return value ? undefined : message
        }
    }
}

validator.minLength = (selector, minLengh, message) => {
    return {
        selector: selector,
        test: (value) => {
            return value.length >= minLengh ? undefined : message
        }
    }
}

validator.confirm = (selector, targetSelector, message) => {
    return {
        selector: selector,
        test : (value) => {
            let target = document.querySelector(targetSelector)
            return value == target.value ? undefined : message
        }
    }
}

validator.differ = (selector, targetSelector, message) => {
    return {
        selector: selector,
        test: (value) => {
            var target = document.querySelector(targetSelector)
            return value != target.value ? undefined : message
        }
    }
}

validator.isEmail = (selector, message) => {
    return {
        selector: selector,
        test: (value) => {
            var emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
            return emailRegex.test(value) ? undefined : message
        }
    }
}



function showFormError(
    options = {
        formSelector: '#form',
        errorSelector: '.form__error',
        errors: undefined,
        errorClass: 'invalid',
    }
) {
    form  = document.querySelector(options.formSelector)
    if (form && options.errors) {
        // console.log(attrs)
        // errorContainer.innerHTML = ''
        console.log(options.errors)
        var inputElements = document.querySelectorAll('input')
        inputElements.forEach(inputElement => {
            var errorElements = [...inputElement.parentNode.querySelectorAll(options.errorSelector)]
            console.log(errorElements)
            errorElements.forEach(e=>e.remove())
            if (options.errors.hasOwnProperty(inputElement.name)){
                errorContainer = inputElement.parentNode
                errorContainer.classList.add(options.errorClass)
                options.errors[inputElement.name].forEach(error => {
                    var newErrorElement = document.createElement('span')
                    newErrorElement.innerText = error
                    newErrorElement.classList.add(options.errorSelector.substring(1))
                    errorContainer.appendChild(newErrorElement)
                })
            }
        })
    }
}
