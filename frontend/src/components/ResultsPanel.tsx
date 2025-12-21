import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, Activity } from "lucide-react";
import GaugeMeter from "./GaugeMeter";

interface ResultsPanelProps {
  prediction: {
    valence: "HIGH" | "LOW";
    confidence: number;
    interpretation: string;
  } | null;
}

const ResultsPanel = ({ prediction }: ResultsPanelProps) => {
  if (!prediction) return null;

  const isHigh = prediction.valence === "HIGH";

  return (
    <section className="py-12 px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, type: "spring" }}
        className="max-w-2xl mx-auto"
      >
        {/* Main Result Card */}
        <div className={`
          glass-panel p-8 md:p-10 relative overflow-hidden
          ${isHigh ? "glow-purple" : "glow-pink"}
        `}>
          {/* Background Gradient */}
          <div className={`
            absolute inset-0 opacity-20
            ${isHigh 
              ? "bg-gradient-to-br from-glow-purple/30 via-transparent to-glow-blue/30"
              : "bg-gradient-to-br from-glow-pink/30 via-transparent to-destructive/30"
            }
          `} />

          {/* Animated Background Particles */}
          <div className="absolute inset-0 overflow-hidden">
            {[...Array(15)].map((_, i) => (
              <motion.div
                key={i}
                className={`absolute w-1 h-1 rounded-full ${isHigh ? "bg-accent" : "bg-destructive"}`}
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                }}
                animate={{
                  opacity: [0, 1, 0],
                  scale: [0, 1.5, 0],
                }}
                transition={{
                  duration: 2 + Math.random() * 2,
                  repeat: Infinity,
                  delay: Math.random() * 2,
                }}
              />
            ))}
          </div>

          {/* Content */}
          <div className="relative z-10">
            {/* Header */}
            <div className="text-center mb-8">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: "spring" }}
                className={`
                  inline-flex items-center gap-2 px-6 py-2 rounded-full mb-4
                  ${isHigh 
                    ? "bg-accent/20 border border-accent/50 text-accent"
                    : "bg-destructive/20 border border-destructive/50 text-destructive"
                  }
                `}
              >
                <Activity className="w-4 h-4" />
                <span className="font-display text-sm tracking-wider">ANALYSIS COMPLETE</span>
              </motion.div>

              <h3 className="font-display text-xl text-muted-foreground mb-2">
                PREDICTED VALENCE
              </h3>

              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="flex items-center justify-center gap-4"
              >
                <motion.div
                  animate={{ rotate: [0, 10, -10, 0] }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  {isHigh ? (
                    <TrendingUp className={`w-12 h-12 ${isHigh ? "text-accent" : "text-destructive"}`} />
                  ) : (
                    <TrendingDown className={`w-12 h-12 ${isHigh ? "text-accent" : "text-destructive"}`} />
                  )}
                </motion.div>

                <h2 className={`
                  font-display text-5xl md:text-7xl font-bold tracking-wider
                  ${isHigh ? "text-accent text-glow-purple" : "text-destructive"}
                `}
                style={!isHigh ? {
                  textShadow: "0 0 10px hsl(var(--destructive) / 0.8), 0 0 20px hsl(var(--destructive) / 0.5)"
                } : {}}
                >
                  {prediction.valence}
                </h2>
              </motion.div>
            </div>

            {/* Gauge Meter */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="flex justify-center mb-8"
            >
              <GaugeMeter 
                value={prediction.confidence} 
                isHigh={isHigh}
              />
            </motion.div>

            {/* Confidence Display */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="text-center mb-6"
            >
              <p className="font-display text-sm text-muted-foreground mb-1">
                CONFIDENCE LEVEL
              </p>
              <p className={`font-display text-3xl font-bold ${isHigh ? "text-accent" : "text-destructive"}`}>
                {(prediction.confidence * 100).toFixed(1)}%
              </p>
            </motion.div>

            {/* Interpretation */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="system-notification text-center"
            >
              <p className="font-body text-foreground/90">
                {prediction.interpretation}
              </p>
            </motion.div>
          </div>

          {/* Decorative Corners */}
          <div className={`absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 rounded-tl-lg ${isHigh ? "border-accent/50" : "border-destructive/50"}`} />
          <div className={`absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 rounded-tr-lg ${isHigh ? "border-accent/50" : "border-destructive/50"}`} />
          <div className={`absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 rounded-bl-lg ${isHigh ? "border-accent/50" : "border-destructive/50"}`} />
          <div className={`absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 rounded-br-lg ${isHigh ? "border-accent/50" : "border-destructive/50"}`} />
        </div>
      </motion.div>
    </section>
  );
};

export default ResultsPanel;
