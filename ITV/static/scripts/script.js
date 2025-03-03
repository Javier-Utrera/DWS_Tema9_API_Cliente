function eliminar() {
    var x = confirm("¿Seguro que quiero eliminarlo ?");
    if (x)
      return true;
    else
      return false;
}

function testCORS() {
  fetch("http://127.0.0.1:8000/api/v1/citas/listar_citas", {
      method: "GET",
      headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer 3o9eIlqpAunV29t4Un5cZjRh3VxwaT"
      }
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
      }
      return response.json();
  })
  .then(data => {
      console.log("Datos recibidos:", data);
      document.getElementById("resultado").innerText = JSON.stringify(data, null, 2);
  })
  .catch(error => {
      console.error("Error en la petición:", error);
      document.getElementById("resultado").innerText = "Error: " + error;
  });
}