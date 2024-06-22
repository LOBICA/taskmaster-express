export interface ConfirmDialog {
  title: string;
  description: string;
  buttons: {
    cancelTitle: string;
    confirmTitle: string;
  }
  buttonColor?: string;
}