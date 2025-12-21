import { motion } from "framer-motion";
import { Download, FileText, CheckCircle } from "lucide-react";
import { useState } from "react";

interface ReportDownloadProps {
  hasResults: boolean;
  onDownload: () => void;
}

const ReportDownload = ({ hasResults, onDownload }: ReportDownloadProps) => {
  const [isDownloading, setIsDownloading] = useState(false);
  const [downloaded, setDownloaded] = useState(false);

  const handleDownload = async () => {
    setIsDownloading(true);
    await new Promise((resolve) => setTimeout(resolve, 1500));
    onDownload();
    setIsDownloading(false);
    setDownloaded(true);
    setTimeout(() => setDownloaded(false), 3000);
  };

  if (!hasResults) return null;

  return (
    <section className="py-12 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-md mx-auto"
      >
        {/* Download Card */}
        <div className="glass-panel p-6 md:p-8 text-center relative overflow-hidden">
          {/* Animated Background */}
          <div className="absolute inset-0 holographic opacity-30" />

          {/* Content */}
          <div className="relative z-10">
            <motion.div
              className="w-16 h-16 mx-auto mb-6 rounded-full bg-primary/20 border border-primary/50 flex items-center justify-center"
              animate={{
                boxShadow: [
                  "0 0 0 0 hsl(var(--primary) / 0)",
                  "0 0 0 15px hsl(var(--primary) / 0.1)",
                  "0 0 0 0 hsl(var(--primary) / 0)",
                ],
              }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <FileText className="w-8 h-8 text-primary" />
            </motion.div>

            <h3 className="font-display text-xl text-foreground mb-2">
              ANALYSIS REPORT
            </h3>
            <p className="font-body text-muted-foreground mb-6">
              Download comprehensive PDF report with all analysis results
            </p>

            {/* Report Contents Preview */}
            <div className="text-left mb-6 space-y-2">
              {[
                "Prediction Results & Confidence",
                "Band Power Contributions",
                "Channel Activation Heatmap",
                "Preprocessing Summary",
              ].map((item, i) => (
                <motion.div
                  key={item}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="flex items-center gap-2 text-sm"
                >
                  <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                  <span className="font-body text-muted-foreground">{item}</span>
                </motion.div>
              ))}
            </div>

            {/* Download Button */}
            <motion.button
              onClick={handleDownload}
              disabled={isDownloading}
              className={`
                w-full py-4 px-6 rounded-xl font-display tracking-wider
                flex items-center justify-center gap-3
                transition-all duration-300
                ${downloaded
                  ? "bg-green-500/20 border border-green-500/50 text-green-400"
                  : "magic-button text-primary-foreground"
                }
              `}
              whileHover={!isDownloading && !downloaded ? { scale: 1.02 } : {}}
              whileTap={!isDownloading && !downloaded ? { scale: 0.98 } : {}}
            >
              {isDownloading ? (
                <>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  >
                    <Download className="w-5 h-5" />
                  </motion.div>
                  <span>GENERATING REPORT...</span>
                </>
              ) : downloaded ? (
                <>
                  <CheckCircle className="w-5 h-5" />
                  <span>DOWNLOAD COMPLETE</span>
                </>
              ) : (
                <>
                  <Download className="w-5 h-5" />
                  <span>DOWNLOAD REPORT</span>
                </>
              )}
            </motion.button>

            {/* File Info */}
            <p className="mt-4 font-body text-xs text-muted-foreground">
              PDF • ~2 MB • Solo Leveling Theme
            </p>
          </div>

          {/* Corner Decorations */}
          <div className="absolute top-0 left-0 w-6 h-6 border-t-2 border-l-2 border-primary/30 rounded-tl-lg" />
          <div className="absolute top-0 right-0 w-6 h-6 border-t-2 border-r-2 border-primary/30 rounded-tr-lg" />
          <div className="absolute bottom-0 left-0 w-6 h-6 border-b-2 border-l-2 border-primary/30 rounded-bl-lg" />
          <div className="absolute bottom-0 right-0 w-6 h-6 border-b-2 border-r-2 border-primary/30 rounded-br-lg" />
        </div>
      </motion.div>
    </section>
  );
};

export default ReportDownload;
