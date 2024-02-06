import ImageKit from 'imagekit';
import { createBlob } from './create-blob';

export type UploadPayload = {
  file?: File;
  fileName?: string | null;
};

export async function uploadFile({
  file,
  fileName,
}: Partial<UploadPayload>): Promise<string | null | undefined> {
  if (!file || !fileName) return

  return new Promise(function (resolve, reject) {
    if (!file || !fileName) throw new Error('Invalid file or filename');

    const imagekit = new ImageKit({
      publicKey: process.env.IMAGE_KIT_PUBLIC_KEY ?? '',
      privateKey: process.env.IMAGE_KIT_PRIVATE_KEY ?? '',
      urlEndpoint: process.env.IMAGE_KIT_URL_ENDPOINT ?? '',
    });

    createBlob(file, async function (blob) {
      try {
        if (blob) {
          const response = await imagekit.upload({ file: blob, fileName });
          resolve(response.url);
        }
      } catch (error) {
        reject(error);
      }
    });
  });
}
