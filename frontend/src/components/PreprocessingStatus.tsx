import { motion } from "framer-motion";
import { Check, Loader2 } from "lucide-react";

interface PreprocessingStep {
  id: string;
  label: string;
  status: "pending" | "processing" | "completed";
}

interface PreprocessingStatusProps {
  steps: PreprocessingStep[];
  isProcessing: boolean;
}

const PreprocessingStatus = ({ steps, isProcessing }: PreprocessingStatusProps) => {
  if (!isProcessing && steps.every(s => s.status === "pending")) {
    return null;
  }

  return (
    <section className="py-12 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-3xl mx-auto"
      >
        {/* Section Header */}
        <div className="text-center mb-8">
          <h3 className="font-display text-2xl md:text-3xl text-primary text-glow-cyan mb-2">
            SIGNAL PROCESSING
          </h3>
          <p className="font-body text-muted-foreground">
            Neural data preprocessing pipeline
          </p>
        </div>

        {/* Timeline */}
        <div className="glass-panel p-6 md:p-8">
          <div className="relative">
            {/* Progress Line */}
            <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-muted">
              <motion.div
                className="absolute top-0 left-0 w-full bg-gradient-to-b from-primary to-accent"
                initial={{ height: "0%" }}
                animate={{
                  height: `${(steps.filter(s => s.status === "completed").length / steps.length) * 100}%`,
                }}
                transition={{ duration: 0.5 }}
              />
            </div>

            {/* Steps */}
            <div className="space-y-6">
              {steps.map((step, index) => (
                <motion.div
                  key={step.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="relative flex items-center gap-4 pl-4"
                >
                  {/* Status Icon */}
                  <motion.div
                    className={`
                      relative z-10 w-10 h-10 rounded-full flex items-center justify-center
                      transition-all duration-300
                      ${step.status === "completed" 
                        ? "bg-primary/20 border-2 border-primary glow-cyan" 
                        : step.status === "processing"
                        ? "bg-accent/20 border-2 border-accent animate-pulse"
                        : "bg-muted border-2 border-muted-foreground/30"
                      }
                    `}
                    animate={step.status === "processing" ? {
                      boxShadow: [
                        "0 0 0 0 hsl(var(--accent) / 0)",
                        "0 0 0 10px hsl(var(--accent) / 0.2)",
                        "0 0 0 0 hsl(var(--accent) / 0)",
                      ],
                    } : {}}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  >
                    {step.status === "completed" ? (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: "spring", stiffness: 500 }}
                      >
                        <Check className="w-5 h-5 text-primary" />
                      </motion.div>
                    ) : step.status === "processing" ? (
                      <Loader2 className="w-5 h-5 text-accent animate-spin" />
                    ) : (
                      <div className="w-2 h-2 rounded-full bg-muted-foreground/30" />
                    )}
                  </motion.div>

                  {/* Label */}
                  <div className="flex-1">
                    <div className="system-notification">
                      <span className={`
                        font-display text-sm tracking-wider
                        ${step.status === "completed" 
                          ? "text-primary" 
                          : step.status === "processing"
                          ? "text-accent"
                          : "text-muted-foreground"
                        }
                      `}>
                        {step.status === "completed" && "✓ "}
                        {step.label}
                      </span>
                    </div>
                  </div>

                  {/* Status Badge */}
                  <motion.div
                    className={`
                      px-3 py-1 rounded-full text-xs font-display tracking-wider
                      ${step.status === "completed"
                        ? "bg-primary/20 text-primary border border-primary/30"
                        : step.status === "processing"
                        ? "bg-accent/20 text-accent border border-accent/30"
                        : "bg-muted text-muted-foreground border border-muted-foreground/30"
                      }
                    `}
                    animate={step.status === "processing" ? { opacity: [0.5, 1, 0.5] } : {}}
                    transition={{ duration: 1, repeat: Infinity }}
                  >
                    {step.status.toUpperCase()}
                  </motion.div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Progress Bar */}
          <div className="mt-8 pt-6 border-t border-border/50">
            <div className="flex justify-between items-center mb-2">
              <span className="font-display text-sm text-muted-foreground">
                PROCESSING PROGRESS
              </span>
              <span className="font-display text-sm text-primary">
                {Math.round((steps.filter(s => s.status === "completed").length / steps.length) * 100)}%
              </span>
            </div>
            <div className="h-2 bg-muted rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-primary via-accent to-primary rounded-full"
                initial={{ width: "0%" }}
                animate={{
                  width: `${(steps.filter(s => s.status === "completed").length / steps.length) * 100}%`,
                }}
                transition={{ duration: 0.5 }}
                style={{
                  backgroundSize: "200% 100%",
                }}
              />
            </div>
          </div>
        </div>
      </motion.div>
    </section>
  );
};

export default PreprocessingStatus;
