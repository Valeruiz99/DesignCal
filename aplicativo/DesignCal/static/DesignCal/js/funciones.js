function confirmar(url){
    if(confirm("¿Está seguro que desea eliminar?")){
        location.href=url
    }
}
function buscar(url){
    dato = $('#dato').val();
    resultado = $('#respuesta');

    token = $('input[name="csrfmiddlewaretoken"').val();
    console.log("Token: "+ token)
    $.ajax({
        url: url,
        type: 'post',
        data: {
            "dato": dato,"csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(respuesta){
            //Sobreescribir el html
            resultado.html(respuesta);
        },
        error: function(e){
            console.log("Error: " + e);
        }
    });
}

