

import { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Upload, Sparkles, Download, Loader2, ImageIcon } from "lucide-react";

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [d0, setD0] = useState("");
  const [a, setA] = useState("");
  const [b, setB] = useState("");
  const [loading, setLoading] = useState(false);
  const [resultUrl, setResultUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (f: File | null) => {
    setFile(f);
    setResultUrl(null);
    setError(null);
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(f ? URL.createObjectURL(f) : null);
  };

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please choose an image first.");
      return;
    }
    setLoading(true);
    setError(null);
    setResultUrl(null);
    try {
      const fd = new FormData();
      fd.append("file", file);
      if (d0) fd.append("d0", d0);
      if (a) fd.append("a", a);
      if (b) fd.append("b", b);
      const res = await fetch("/api/enhance", { method: "POST", body: fd });
      const text = await res.text();
      if (!res.ok) throw new Error(text || `Request failed (${res.status})`);
      const json = JSON.parse(text);
      if (!json.url) throw new Error("No URL in response");
      setResultUrl(json.url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen px-6 py-12 md:py-20">
      <div className="mx-auto max-w-6xl">
        <header className="mb-12 text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-border bg-card/40 px-4 py-1.5 text-xs font-medium text-muted-foreground backdrop-blur">
            <Sparkles className="h-3.5 w-3.5 text-primary" />
            Image enhancement
          </div>
          <h1 className="mt-6 bg-gradient-to-br from-foreground to-muted-foreground bg-clip-text text-5xl font-semibold tracking-tight text-transparent md:text-6xl">
            PGM Enhancement
          </h1>
          <p className="mx-auto mt-4 max-w-xl text-balance text-muted-foreground">
            Upload a PGM, PNG, or JPG, tune the parameters, and get a beautifully enhanced image back.
          </p>
        </header>

        <div className="grid gap-6 md:grid-cols-2">
          <Card className="overflow-hidden border-border bg-card/60 p-6 backdrop-blur-xl" style={{ boxShadow: "var(--shadow-card)" }}>
            <form onSubmit={submit} className="space-y-6">
              <div>
                <Label className="mb-2 block text-sm font-medium">Image</Label>
                <button
                  type="button"
                  onClick={() => inputRef.current?.click()}
                  className="group relative flex h-48 w-full items-center justify-center overflow-hidden rounded-lg border border-dashed border-border bg-background/40 transition hover:border-primary/60 hover:bg-background/60"
                >
                  {previewUrl ? (
                    <img src={previewUrl} alt="preview" className="h-full w-full object-contain" />
                  ) : (
                    <div className="flex flex-col items-center gap-2 text-muted-foreground">
                      <Upload className="h-6 w-6" />
                      <span className="text-sm">{file ? file.name : "Click to upload PGM, PNG or JPG"}</span>
                    </div>
                  )}
                </button>
                <input
                  ref={inputRef}
                  type="file"
                  accept=".pgm,image/png,image/jpeg"
                  className="hidden"
                  onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
                />
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <Label htmlFor="d0" className="mb-1.5 block text-xs text-muted-foreground">d0</Label>
                  <Input id="d0" type="number" step="any" value={d0} onChange={(e) => setD0(e.target.value)} placeholder="—" />
                </div>
                <div>
                  <Label htmlFor="a" className="mb-1.5 block text-xs text-muted-foreground">a</Label>
                  <Input id="a" type="number" step="any" value={a} onChange={(e) => setA(e.target.value)} placeholder="—" />
                </div>
                <div>
                  <Label htmlFor="b" className="mb-1.5 block text-xs text-muted-foreground">b</Label>
                  <Input id="b" type="number" step="any" value={b} onChange={(e) => setB(e.target.value)} placeholder="—" />
                </div>
              </div>

              <Button
                type="submit"
                disabled={loading || !file}
                className="w-full text-primary-foreground"
                style={{ background: "var(--gradient-primary)", boxShadow: "var(--shadow-glow)" }}
              >
                {loading ? (
                  <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Enhancing…</>
                ) : (
                  <><Sparkles className="mr-2 h-4 w-4" /> Enhance image</>
                )}
              </Button>

              {error && (
                <p className="rounded-md border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive-foreground">
                  {error}
                </p>
              )}
            </form>
          </Card>

          <Card className="flex flex-col overflow-hidden border-border bg-card/60 p-6 backdrop-blur-xl" style={{ boxShadow: "var(--shadow-card)" }}>
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-sm font-medium">Result</h2>
              {resultUrl && (
                <a
                  href={resultUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1.5 text-xs text-primary hover:underline"
                >
                  <Download className="h-3.5 w-3.5" /> Open
                </a>
              )}
            </div>
            <div className="flex flex-1 items-center justify-center rounded-lg border border-border bg-background/40 p-3 min-h-[300px]">
              {loading ? (
                <div className="flex flex-col items-center gap-3 text-muted-foreground">
                  <Loader2 className="h-6 w-6 animate-spin" />
                  <span className="text-sm">Working its magic…</span>
                </div>
              ) : resultUrl ? (
                <img src={resultUrl} alt="enhanced" className="max-h-[480px] w-full object-contain" />
              ) : (
                <div className="flex flex-col items-center gap-2 text-muted-foreground">
                  <ImageIcon className="h-6 w-6" />
                  <span className="text-sm">Your enhanced image will appear here</span>
                </div>
              )}
            </div>
          </Card>
        </div>
      </div>
    </main>
  );
}
