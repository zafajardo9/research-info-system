export function createBlob(file: File, callback: (result: any) => any) {
  const reader = new FileReader();

  reader.onload = function () {
    callback(reader.result);
  };

  reader.readAsDataURL(file);
}
