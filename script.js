document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('uploadForm').addEventListener('submit', function(event) {
        event.preventDefault();
        let formData = new FormData(this);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                Swal.fire({
                    title: 'Upload Status',
                    text: data.message + ' Your file code is: ' + data.fileCode,
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(() => location.reload());
            } else {
                Swal.fire({ title: 'Upload Status', text: data.message, icon: 'error', confirmButtonText: 'OK' });
            }
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('shareTextForm').addEventListener('submit', function(event) {
        event.preventDefault();
        let formData = new FormData(this);

        fetch('/share', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                Swal.fire({
                    title: 'Share Text Status',
                    text: data.message + ' Your text code is: ' + data.textCode,
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(() => location.reload());
            } else {
                Swal.fire({ title: 'Share Text Status', text: data.message, icon: 'error', confirmButtonText: 'OK' });
            }
        })
        .catch(error => console.error('Error:', error));
    });

    fetch('/visitor-count')
    .then(response => response.text())
    .then(data => {
        document.getElementById('count').textContent = data;
    })
    .catch(error => console.error('Error fetching visitor count:', error));
});
