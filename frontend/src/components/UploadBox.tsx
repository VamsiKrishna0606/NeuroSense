import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, FileText, X, Check } from "lucide-react";

interface UploadBoxProps {
  onFileSelect: (file: File | null) => void;
  selectedFile: File | null;
}

const UploadBox = ({ onFileSelect, selectedFile }: UploadBoxProps) => {
  const [isDragActive, setIsDragActive] = useState(false);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0]);
      }
    },
    [onFileSelect]
  );

  const { getRootProps, getInputProps, open } = useDropzone({
    onDrop,
    onDragEnter: () => setIsDragActive(true),
    onDragLeave: () => setIsDragActive(false),
    accept: {
      "text/csv": [".csv"],
      "application/x-matlab-data": [".mat"],
    },
    multiple: false,
    noClick: !!selectedFile,
  });

  const removeFile = () => {
    onFileSelect(null);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  };

  return (
    <section className="py-12 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-2xl mx-auto"
      >
        {/* Section Header */}
        <div className="text-center mb-8">
          <h3 className="font-display text-2xl md:text-3xl text-primary text-glow-cyan mb-2">
            UPLOAD EEG DATA
          </h3>
          <p className="font-body text-muted-foreground">
            Drag and drop your neural signal file
          </p>
        </div>

        {/* Upload Zone */}
        <motion.div
          whileHover={{ scale: selectedFile ? 1 : 1.01 }}
          whileTap={{ scale: 0.99 }}
        >
          <div
            {...getRootProps()}
            className={`
              relative glass-panel p-8 md:p-12 cursor-pointer
              transition-all duration-300 group
              ${isDragActive ? "glow-cyan border-primary" : "hover:border-primary/50"}
              ${selectedFile ? "border-green-500/50" : ""}
            `}
          >
          <input {...getInputProps()} />

          {/* Animated EEG Background */}
          <div className="absolute inset-0 overflow-hidden rounded-xl opacity-20">
            <svg className="w-full h-full" preserveAspectRatio="none">
              <motion.path
                d="M0,50 Q25,30 50,50 T100,50 T150,50 T200,50 T250,50 T300,50 T350,50 T400,50"
                fill="none"
                stroke="hsl(var(--primary))"
                strokeWidth="2"
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ 
                  pathLength: 1, 
                  opacity: [0.3, 0.6, 0.3],
                  d: [
                    "M0,50 Q25,30 50,50 T100,50 T150,50 T200,50 T250,50 T300,50 T350,50 T400,50",
                    "M0,50 Q25,70 50,50 T100,50 T150,50 T200,50 T250,50 T300,50 T350,50 T400,50",
                    "M0,50 Q25,30 50,50 T100,50 T150,50 T200,50 T250,50 T300,50 T350,50 T400,50",
                  ]
                }}
                transition={{ 
                  duration: 3, 
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
            </svg>
          </div>

          {/* Drag Active Overlay */}
          <AnimatePresence>
            {isDragActive && (
              <motion.div
                className="absolute inset-0 bg-primary/10 rounded-xl flex items-center justify-center"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                <div className="text-center">
                  <Upload className="w-16 h-16 text-primary mx-auto animate-bounce" />
                  <p className="font-display text-primary mt-4">DROP FILE HERE</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Content */}
          <AnimatePresence mode="wait">
            {!selectedFile ? (
              <motion.div
                key="upload"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="relative z-10 text-center"
              >
                <motion.div
                  className="w-20 h-20 mx-auto mb-6 rounded-full border-2 border-dashed border-primary/50 flex items-center justify-center group-hover:border-primary transition-colors"
                  animate={{
                    boxShadow: [
                      "0 0 0 0 hsl(var(--primary) / 0)",
                      "0 0 0 10px hsl(var(--primary) / 0.1)",
                      "0 0 0 0 hsl(var(--primary) / 0)",
                    ],
                  }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  <Upload className="w-8 h-8 text-primary" />
                </motion.div>

                <p className="font-display text-lg text-foreground mb-2">
                  DRAG & DROP EEG FILE
                </p>
                <p className="font-body text-muted-foreground mb-4">
                  or click to browse
                </p>

                {/* File Types */}
                <div className="flex justify-center gap-4">
                  <span className="px-3 py-1 rounded-full border border-primary/30 text-primary text-sm font-display">
                    .MAT
                  </span>
                  <span className="px-3 py-1 rounded-full border border-primary/30 text-primary text-sm font-display">
                    .CSV
                  </span>
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="file"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="relative z-10"
              >
                <div className="flex items-center justify-between gap-4">
                  <div className="flex items-center gap-4">
                    <div className="w-14 h-14 rounded-lg bg-green-500/20 border border-green-500/50 flex items-center justify-center">
                      <FileText className="w-7 h-7 text-green-400" />
                    </div>
                    <div className="text-left">
                      <p className="font-display text-foreground truncate max-w-[200px] md:max-w-[300px]">
                        {selectedFile.name}
                      </p>
                      <p className="font-body text-sm text-muted-foreground">
                        {formatFileSize(selectedFile.size)}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <motion.div
                      className="w-10 h-10 rounded-full bg-green-500/20 border border-green-500/50 flex items-center justify-center"
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: 0.2, type: "spring" }}
                    >
                      <Check className="w-5 h-5 text-green-400" />
                    </motion.div>

                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        removeFile();
                      }}
                      className="w-10 h-10 rounded-full bg-destructive/20 border border-destructive/50 flex items-center justify-center hover:bg-destructive/30 transition-colors"
                    >
                      <X className="w-5 h-5 text-destructive" />
                    </button>
                  </div>
                </div>

                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    open();
                  }}
                  className="mt-4 font-display text-sm text-primary hover:text-primary/80 transition-colors"
                >
                  CHOOSE DIFFERENT FILE
                </button>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Corner Decorations */}
          <div className="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-primary/50 rounded-tl-lg" />
          <div className="absolute top-0 right-0 w-4 h-4 border-t-2 border-r-2 border-primary/50 rounded-tr-lg" />
          <div className="absolute bottom-0 left-0 w-4 h-4 border-b-2 border-l-2 border-primary/50 rounded-bl-lg" />
          <div className="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-primary/50 rounded-br-lg" />
          </div>
        </motion.div>
      </motion.div>
    </section>
  );
};

export default UploadBox;
