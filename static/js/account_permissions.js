async function userPermissions() {
    try {
        const response = await fetch('/permissions/list');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const permissions = data.permissions || [];  // Ensure permissions is an array
        const permissionsSelect = document.getElementById('permissions_select');
        const permissionsButton = document.getElementById('permissions_button');

        permissionsSelect.innerHTML = '';

        permissions.forEach(permission => {
            const option = document.createElement('option');
            option.value = permission;
            option.textContent = permission;
            permissionsSelect.appendChild(option);
        });
        // 默认选中
        updateButtonLabel('player.*');

    } catch (error) {
        console.error('获取权限失败:', error);
    }
}

function toggleDropdown() {
    const dropdown = document.getElementById('permissions_select');
    const button = document.getElementById('permissions_button');
    dropdown.classList.toggle('show');
    button.classList.toggle('active');
}

function updateButtonLabel(label) {
    document.getElementById('permissions_button').textContent = label;
}

function handleSelectionChange() {
    const select = document.getElementById('permissions_select');
    const selectedOptions = Array.from(select.selectedOptions).map(option => option.value);
    const displayText = selectedOptions.length > 0 ? selectedOptions.join(', ') : 'player.*';
    updateButtonLabel(displayText);

    const dropdown = document.getElementById('permissions_select');
    const button = document.getElementById('permissions_button');
    dropdown.classList.remove('show');
    button.classList.remove('active');
}

async function updatePermissions(action) {
    const username = document.getElementById('update_username').value;
    const selectedPermissions = Array.from(document.getElementById('permissions_select').selectedOptions)
        .map(option => option.value);

    if (!username) {
        Swal.fire("提交失败", "用户名不能为空", "error")
        return;
    }

    try {
        const response = await fetch('/permissions/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                permissions: selectedPermissions,
                action: action
            })
        });
        const result = await response.json();
        if (result.status === 'success') {
            Swal.fire("提交成功", result.message, "success")
        } else {
            Swal.fire("提交失败", result.message || "未知错误", "error")
        }
    } catch (error) {
        console.error('更新权限失败:', error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    userPermissions();
    document.getElementById('permissions_select').addEventListener('change', handleSelectionChange);
});
