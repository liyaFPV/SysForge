function fetchData() {
    fetch("/api")
        .then(response => response.json())
        .then(data => {
            document.getElementById("cpu").innerText = data.CPU_usage;
            document.getElementById("ram").innerText = 
                `${data.RAM_used} / ${data.RAM_total} (${data.RAM_percent})`;

            const disksDiv = document.getElementById("disks");
            disksDiv.innerHTML = "";
            data.Disks.forEach(disk => {
                let html = `<h3>${disk.disk}</h3>`;
                disk.partitions.forEach(p => {
                    html += `<p>${p.device} (${p.mountpoint}): ${p.used} / ${p.total} (${p.percent})</p>`;
                });
                disksDiv.innerHTML += html;
            });

            console.log("CPU:", data.CPU_usage);
            console.log("RAM:", data.RAM_used, "/", data.RAM_total, `(${data.RAM_percent})`);
            data.Disks.forEach(disk => {
                console.log("Диск:", disk.disk);
                disk.partitions.forEach(p => {
                    console.log("  Раздел:", p.device, "| Точка:", p.mountpoint, "| Использование:", p.used, "/", p.total, `(${p.percent})`);
                });
            });
        })
        .catch(err => console.error("Ошибка при получении данных:", err));
}

fetchData();

setInterval(fetchData, 500);