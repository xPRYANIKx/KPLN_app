const verificationDialog = document.getElementById('verification_dialog');
const paragraphQuestion = document.getElementById('paragraph_question');
const cancelDialogBtn = document.getElementById('verification_dialog__cancel');
const nextDialogBtn = document.getElementById('verification_dialog__next');

const paymentForm = document.getElementById('paymentForm');
const dsubmit_button_in_form = document.getElementById('submitButton');

const annulEditBtn = document.getElementById('annul__edit_btn_i');
const annulApprovalEditBtn = document.getElementById('annul_approval__edit_btn_i');
const saveEditBtn = document.getElementById('save__edit_btn_i');


const hideDialog = () => {
    verificationDialog.close();
};
cancelDialogBtn.addEventListener('click', hideDialog);


const showDialogDSB = () => {
    verificationDialog.showModal();
    paragraphQuestion.id = 'pqDSB'
};
dsubmit_button_in_form.addEventListener('click', showDialogDSB);
const showDialogAEB = () => {
    verificationDialog.showModal();
    paragraphQuestion.id = 'pqAEB'
};
annulEditBtn.addEventListener('click', showDialogAEB);
const showDialogAPEB = () => {
    verificationDialog.showModal();
    paragraphQuestion.id = 'pqAPEB'
};
annulApprovalEditBtn.addEventListener('click', showDialogAPEB);
const showDialogSEB = () => {
    verificationDialog.showModal();
    paragraphQuestion.id = 'pqSEB'
};
saveEditBtn.addEventListener('click', showDialogSEB);


nextDialogBtn.addEventListener('click', function () {
    if (paragraphQuestion.id === 'pqDSB') {
        paymentForm.submit();
    } else if (paragraphQuestion.id === 'pqAEB') {
        annulPayment();
    } else if (paragraphQuestion.id === 'pqAPEB') {
        annulApproval();
    } else if (paragraphQuestion.id === 'pqSEB') {
        savePayment();
    }
});