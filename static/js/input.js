function validateInput(input) {
    input.value = input.value.replace(/[^0-9]/g, '');  // 只允许输入数字
}