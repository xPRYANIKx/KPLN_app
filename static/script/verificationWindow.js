const verificationDialog = document.getElementById('verification_dialog');
const paragraphQuestion = document.getElementById('paragraph_question');
const cancelDialogBtn = document.getElementById('verification_dialog__cancel');
const nextDialogBtn = document.getElementById('verification_dialog__next');

const paymentForm = document.getElementById('paymentForm');
const submit_button_in_form = document.getElementById('submitButton');


const annulEditBtn = document.getElementById('annul__edit_btn_i');
const annulApprovalEditBtn = document.getElementById('annul_approval__edit_btn_i');
const saveEditBtn = document.getElementById('save__edit_btn_i');

console.log(saveEditBtn)


const hideDialog = () => {
    verificationDialog.close();
};
cancelDialogBtn.addEventListener('click', hideDialog);

const showDialogDSB = () => {
    verificationDialog.showModal();
    paragraphQuestion.id = 'pqDSB'
};
submit_button_in_form.addEventListener('click', showDialogDSB);

const showDialogAEB = () => {
    verificationDialog.showModal();
    paragraphQuestion.id = 'pqAEB'
};
try {
    annulEditBtn.addEventListener('click', showDialogAEB);
    const showDialogAPEB = () => {
        verificationDialog.showModal();
        paragraphQuestion.id = 'pqAPEB'
    };
} catch (err) {

}
try {
    annulApprovalEditBtn.addEventListener('click', showDialogAPEB);
    const showDialogSEB = () => {
        verificationDialog.showModal();
        paragraphQuestion.id = 'pqSEB'
    };
} catch (err) {

}

try {
    console.log(22)
    saveEditBtn.addEventListener('click', showDialogSEB);
    console.log(12)
} catch (err) {

}

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