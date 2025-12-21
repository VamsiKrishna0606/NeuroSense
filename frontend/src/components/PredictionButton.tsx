import { motion } from "framer-motion";
import { Zap, Brain, Loader2 } from "lucide-react";

interface PredictionButtonProps {
  disabled: boolean;
  isLoading: boolean;
  onClick: () => void;
}

const PredictionButton = ({ disabled, isLoading, onClick }: PredictionButtonProps) => {
  return (
    <section className="py-12 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-md mx-auto text-center"
      >
        <motion.button
          onClick={onClick}
          disabled={disabled || isLoading}
          className={`
            relative w-full py-6 px-8 rounded-xl font-display text-xl tracking-widest
            transition-all duration-300 overflow-hidden group
            ${disabled || isLoading
              ? "bg-muted text-muted-foreground cursor-not-allowed"
              : "magic-button text-primary-foreground"
            }
          `}
          whileHover={!disabled && !isLoading ? { scale: 1.02 } : {}}
          whileTap={!disabled && !isLoading ? { scale: 0.98 } : {}}
        >
          {/* Background Energy Effect */}
          {!disabled && !isLoading && (
            <>
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-primary via-glow-blue to-primary opacity-0 group-hover:opacity-100 transition-opacity"
                animate={{
                  backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
                }}
                transition={{ duration: 3, repeat: Infinity }}
                style={{ backgroundSize: "200% 100%" }}
              />
              
              {/* Charging Particles */}
              <div className="absolute inset-0 overflow-hidden">
                {[...Array(10)].map((_, i) => (
                  <motion.div
                    key={i}
                    className="absolute w-1 h-1 bg-foreground rounded-full opacity-0 group-hover:opacity-100"
                    style={{
                      left: `${Math.random() * 100}%`,
                      bottom: 0,
                    }}
                    animate={{
                      y: [0, -80],
                      opacity: [0, 1, 0],
                    }}
                    transition={{
                      duration: 1 + Math.random(),
                      repeat: Infinity,
                      delay: Math.random() * 0.5,
                    }}
                  />
                ))}
              </div>
            </>
          )}

          {/* Button Content */}
          <span className="relative z-10 flex items-center justify-center gap-4">
            {isLoading ? (
              <>
                <Loader2 className="w-6 h-6 animate-spin" />
                <span>ANALYZING NEURAL PATTERNS...</span>
              </>
            ) : (
              <>
                <motion.div
                  animate={!disabled ? {
                    scale: [1, 1.2, 1],
                    opacity: [0.8, 1, 0.8],
                  } : {}}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  {disabled ? <Brain className="w-6 h-6" /> : <Zap className="w-6 h-6" />}
                </motion.div>
                <span>RUN PREDICTION</span>
                <motion.div
                  animate={!disabled ? {
                    scale: [1, 1.2, 1],
                    opacity: [0.8, 1, 0.8],
                  } : {}}
                  transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
                >
                  {disabled ? <Brain className="w-6 h-6" /> : <Zap className="w-6 h-6" />}
                </motion.div>
              </>
            )}
          </span>

          {/* Border Glow */}
          {!disabled && !isLoading && (
            <motion.div
              className="absolute inset-0 rounded-xl"
              style={{
                boxShadow: "inset 0 0 20px hsl(var(--primary) / 0.3)",
              }}
              animate={{
                boxShadow: [
                  "inset 0 0 20px hsl(var(--primary) / 0.3)",
                  "inset 0 0 40px hsl(var(--primary) / 0.5)",
                  "inset 0 0 20px hsl(var(--primary) / 0.3)",
                ],
              }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          )}

          {/* Corner Accents */}
          <div className="absolute top-2 left-2 w-3 h-3 border-t-2 border-l-2 border-primary-foreground/30 rounded-tl" />
          <div className="absolute top-2 right-2 w-3 h-3 border-t-2 border-r-2 border-primary-foreground/30 rounded-tr" />
          <div className="absolute bottom-2 left-2 w-3 h-3 border-b-2 border-l-2 border-primary-foreground/30 rounded-bl" />
          <div className="absolute bottom-2 right-2 w-3 h-3 border-b-2 border-r-2 border-primary-foreground/30 rounded-br" />
        </motion.button>

        {/* Status Text */}
        {disabled && !isLoading && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-4 font-body text-sm text-muted-foreground"
          >
            Upload an EEG file to begin analysis
          </motion.p>
        )}

        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-6"
          >
            {/* EEG Wave Animation */}
            <svg className="w-full h-12" viewBox="0 0 400 50" preserveAspectRatio="none">
              <motion.path
                d="M0,25 Q20,10 40,25 T80,25 T120,25 T160,25 T200,25 T240,25 T280,25 T320,25 T360,25 T400,25"
                fill="none"
                stroke="hsl(var(--primary))"
                strokeWidth="2"
                animate={{
                  d: [
                    "M0,25 Q20,10 40,25 T80,25 T120,25 T160,25 T200,25 T240,25 T280,25 T320,25 T360,25 T400,25",
                    "M0,25 Q20,40 40,25 T80,25 T120,25 T160,25 T200,25 T240,25 T280,25 T320,25 T360,25 T400,25",
                    "M0,25 Q20,10 40,25 T80,25 T120,25 T160,25 T200,25 T240,25 T280,25 T320,25 T360,25 T400,25",
                  ],
                  pathLength: [0.8, 1, 0.8],
                }}
                transition={{ duration: 1.5, repeat: Infinity }}
              />
            </svg>
          </motion.div>
        )}
      </motion.div>
    </section>
  );
};

export default PredictionButton;
