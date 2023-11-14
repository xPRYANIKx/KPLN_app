const verificationDialog = document.getElementById('verification_dialog');
const paragraphQuestion = document.getElementById('paragraph_question');
const cancelDialogBtn = document.getElementById('verification_dialog__cancel');
const nextDialogBtn = document.getElementById('verification_dialog__next');

const paymentForm = document.getElementById('paymentForm');
const submit_button_in_form = document.getElementById('submitButton');

const annulEditBtn = document.getElementById('annul__edit_btn_i');
const annulApprovalEditBtn = document.getElementById('annul_approval__edit_btn_i');
const saveEditBtn = document.getElementById('save__edit_btn_i');

const hideDialog = () => {
    verificationDialog.close();
};

const showDialogDSB = () => {
    verificationDialog.showModal();
    paragraphQuestion.id = 'pqDSB'
};

const showDialogAEB = () => {
    verificationDialog.showModal();
    paragraphQuestion.id = 'pqAEB'
};

const showDialogAPEB = () => {
    verificationDialog.showModal();
    paragraphQuestion.id = 'pqAPEB'
};

const showDialogSEB = () => {
    verificationDialog.showModal();
    paragraphQuestion.id = 'pqSEB'
};

submit_button_in_form? submit_button_in_form.addEventListener('click', showDialogDSB): 1;

cancelDialogBtn? cancelDialogBtn.addEventListener('click', hideDialog): 1;

annulEditBtn? annulEditBtn.addEventListener('click', showDialogAEB): 1;

annulApprovalEditBtn? annulApprovalEditBtn.addEventListener('click', showDialogAPEB): 1;

saveEditBtn? saveEditBtn.addEventListener('click', showDialogSEB): 1;

nextDialogBtn? nextDialogBtn.addEventListener('click', function () {

    if (paragraphQuestion.id === 'pqDSB') {
        paymentForm.submit();

    } else if (paragraphQuestion.id === 'pqAEB') {
        annulPayment();
    } else if (paragraphQuestion.id === 'pqAPEB') {
        annulApproval();
    } else if (paragraphQuestion.id === 'pqSEB') {
        savePayment();
    }
}): 1;