import axios from "axios";

const API_BASE_URL =
  "https://pgm-app-erdybdehcjd0dkch.uaenorth-01.azurewebsites.net";

export interface EnhanceResponse {
  url: string;
}

/**
 * Posts an image file to the /api/enhance endpoint.
 * Returns the Cloudinary URL of the enhanced image.
 */
export async function enhanceImage(file: File): Promise<string> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post<EnhanceResponse>(
    `${API_BASE_URL}/api/enhance`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      timeout: 120_000, // 2 minutes — image processing can be slow
    }
  );

  return response.data.url;
}

/**
 * Downloads an image from a URL and triggers a browser download.
 */
export async function downloadImage(
  imageUrl: string,
  filename: string = "enhanced-image.png"
): Promise<void> {
  const response = await axios.get(imageUrl, {
    responseType: "blob",
  });

  const blob = new Blob([response.data]);
  const blobUrl = URL.createObjectURL(blob);

  const anchor = document.createElement("a");
  anchor.href = blobUrl;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);

  URL.revokeObjectURL(blobUrl);
}
