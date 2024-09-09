async function deleteAccount() {
    const username = document.getElementById('delete_username').value;

    const result = await Swal.fire({
        title: "你确定要删除吗？",
        text: "删除后将无法恢复！",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "是的，删除！",
        cancelButtonText: "取消",
    });

    if (result.isConfirmed) {
        // 如果用户确认删除，执行删除操作
        const response = await fetch('/accounts/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username })
        });
        const result = await response.json();

        if (result.status === 'success') {
            Swal.fire("提交成功", `用户 ${username} 已删除`, "success")
        } else {
            Swal.fire("提交失败", result.message ||"", "error")
        }
    } else {
        Swal.fire("已取消", "", "info")
    }
}
