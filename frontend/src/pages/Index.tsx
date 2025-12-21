import { useState, useCallback } from "react";
import { motion } from "framer-motion";
import { toast } from "@/hooks/use-toast";

import HeroSection from "@/components/HeroSection";
import UploadBox from "@/components/UploadBox";
import PreprocessingStatus from "@/components/PreprocessingStatus";
import PredictionButton from "@/components/PredictionButton";
import ResultsPanel from "@/components/ResultsPanel";
import BandContribution from "@/components/BandContribution";
import ChannelHeatmap from "@/components/ChannelHeatmap";
import ReportDownload from "@/components/ReportDownload";

interface PreprocessingStep {
  id: string;
  label: string;
  status: "pending" | "processing" | "completed";
}

interface PredictionResult {
  valence: "HIGH" | "LOW";
  confidence: number;
  interpretation: string;
}

const initialSteps: PreprocessingStep[] = [
  { id: "load", label: "Loading EEG File", status: "pending" },
  { id: "filter", label: "Bandpass Filtering", status: "pending" },
  { id: "artifact", label: "Artifact Removal", status: "pending" },
  { id: "features", label: "Feature Extraction", status: "pending" },
  { id: "predict", label: "Model Prediction", status: "pending" },
];

const BACKEND_URL = "http://127.0.0.1:5000";

const Index = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileId, setFileId] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [steps, setSteps] = useState<PreprocessingStep[]>(initialSteps);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);

  /* =============================
     FILE UPLOAD
  ============================== */
  const handleFileSelect = useCallback(async (file: File | null) => {
    if (!file) return;

    setSelectedFile(file);
    setPrediction(null);
    setSteps(initialSteps);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${BACKEND_URL}/api/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setFileId(data.fileId);

      toast({
        title: "File Uploaded",
        description: "EEG file uploaded successfully",
      });
    } catch {
      toast({
        title: "Upload Failed",
        description: "Could not upload EEG file",
        variant: "destructive",
      });
    }
  }, []);

  /* =============================
     RUN PREDICTION
  ============================== */
  const runPrediction = async () => {
    if (!fileId) return;

    setIsProcessing(true);
    setPrediction(null);

    try {
      const res = await fetch(`${BACKEND_URL}/api/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fileId }),
      });

      const result = await res.json();
      setPrediction(result);

      toast({
        title: "Analysis Complete",
        description: "Neural pattern analysis finished successfully",
      });
    } catch {
      toast({
        title: "Prediction Failed",
        description: "Error during model inference",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  /* =============================
     DOWNLOAD REPORT
  ============================== */
  const handleDownload = () => {
    if (!fileId) return;

    window.open(
      `${BACKEND_URL}/api/report/${fileId}`,
      "_blank"
    );
  };

  return (
    <div className="min-h-screen relative">
      {/* Background Effects */}
      <div className="fixed inset-0 bg-cyber-grid opacity-20 pointer-events-none" />
      <div className="fixed top-0 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed bottom-0 right-1/4 w-96 h-96 bg-accent/5 rounded-full blur-3xl pointer-events-none" />

      {/* Main Content */}
      <motion.main
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="relative z-10 pb-20"
      >
        <HeroSection />

        <UploadBox
          onFileSelect={handleFileSelect}
          selectedFile={selectedFile}
        />

        <PreprocessingStatus
          steps={steps}
          isProcessing={isProcessing}
        />

        <PredictionButton
          disabled={!fileId}
          isLoading={isProcessing}
          onClick={runPrediction}
        />

        <ResultsPanel prediction={prediction} />

        {/* Backend does not return band data yet */}
        <BandContribution bands={[]} />

        {prediction && <ChannelHeatmap channels={[]} />}

        <ReportDownload
          hasResults={!!prediction}
          onDownload={handleDownload}
        />
      </motion.main>

      {/* Footer */}
      <footer className="relative z-10 py-8 text-center border-t border-border/30">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <p className="font-display text-sm text-muted-foreground tracking-wider">
            NEUROSENSE • EEG EMOTION INTELLIGENCE SYSTEM
          </p>
          <p className="font-body text-xs text-muted-foreground/60 mt-2">
            Solo Leveling Inspired Interface • Neural Pattern Analysis
          </p>
        </motion.div>
      </footer>
    </div>
  );
};

export default Index;
