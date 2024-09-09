async function createAccounts() {
    const count = document.getElementById('create_count').value;
    const response = await fetch('/accounts/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ count: parseInt(count) })
    });
    const result = await response.json();
    if (result.status === 'success') {
        Swal.fire({
            title: "提交成功",
            text: "账号文件已自动下载，弹窗将在 2s 后自动关闭",
            icon: "success",
            timer: 2000,
            timerProgressBar: true,
            willClose: () => {
                // 在弹窗关闭后执行下载
                window.location.href = '/accounts/download';
            }
        });
    } else {
        Swal.fire("提交失败", result.message || "未知错误", "error")
    }
}