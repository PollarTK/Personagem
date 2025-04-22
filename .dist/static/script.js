function verificarSenhas() {
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmar_senha').value;
    
    if (senha !== confirmarSenha) {
        alert("As senhas não são iguais.");
        return false;  // Impede o envio do formulário
    }
    return true;  // Permite o envio do formulário
}
function getActiveSlideIndex() {
    const carousel = document.getElementById('carouselExampleFade');
    const activeSlide = carousel.querySelector('.carousel-item.active img');
  
  if (activeSlide) {
    const activeImageId = activeSlide.id; // Obtém o id da imagem ativa
    console.log('ID da imagem ativa:', activeImageId);

    // Seleciona o campo do formulário onde você deseja enviar o id
    const activeImageIdInput = document.getElementById('variacao');
    activeImageIdInput.value = activeImageId; // Atribui o id ao campo do formulário

    return activeImageId;
} else {
    console.log('Nenhuma imagem ativa encontrada.');
    return -1;
}
}

// Adiciona um manipulador de eventos ao botão de envio
document.getElementById('salvar').addEventListener('click', function(event) {
    event.preventDefault(); // Impede o envio padrão do formulário
    getActiveSlideIndex(); // Chama a função para obter o id da imagem ativa

    // Agora você pode enviar o formulário
    document.getElementById('criar').submit(); // Envia o formulário
});