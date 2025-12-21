import { motion } from "framer-motion";
import { Brain } from "lucide-react";

const HeroSection = () => {
  return (
    <section className="relative min-h-[60vh] flex flex-col items-center justify-center py-20 overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-cyber-grid bg-cyber-grid opacity-30" />
      
      {/* Radial Glow Behind Brain */}
      <motion.div
        className="absolute w-[600px] h-[600px] rounded-full"
        style={{
          background: "radial-gradient(circle, hsl(195 100% 55% / 0.15) 0%, transparent 70%)",
        }}
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.5, 0.8, 0.5],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      {/* Secondary Glow */}
      <motion.div
        className="absolute w-[400px] h-[400px] rounded-full"
        style={{
          background: "radial-gradient(circle, hsl(260 80% 60% / 0.1) 0%, transparent 70%)",
        }}
        animate={{
          scale: [1.2, 1, 1.2],
          opacity: [0.3, 0.6, 0.3],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 0.5,
        }}
      />

      {/* Animated Brain Icon */}
      <motion.div
        className="relative z-10 mb-8"
        initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
      >
        <motion.div
          className="relative"
          animate={{ y: [0, -10, 0] }}
          transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
        >
          {/* Outer Ring */}
          <motion.div
            className="absolute -inset-8 rounded-full border border-primary/30"
            animate={{ rotate: 360 }}
            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          />
          
          {/* Inner Ring */}
          <motion.div
            className="absolute -inset-4 rounded-full border border-primary/50"
            animate={{ rotate: -360 }}
            transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
          />

          {/* Brain Container */}
          <div className="relative p-8 rounded-full glass-panel glow-cyan">
            <Brain className="w-24 h-24 md:w-32 md:h-32 text-primary animate-brain-pulse" strokeWidth={1} />
            
            {/* Scan Line Effect */}
            <div className="absolute inset-0 rounded-full overflow-hidden">
              <motion.div
                className="absolute inset-x-0 h-1 bg-gradient-to-b from-transparent via-primary/50 to-transparent"
                animate={{ y: ["-100%", "200%"] }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              />
            </div>
          </div>

          {/* Orbiting Particles */}
          {[...Array(6)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-2 h-2 rounded-full bg-primary"
              style={{
                top: "50%",
                left: "50%",
              }}
              animate={{
                rotate: 360,
              }}
              transition={{
                duration: 8 + i * 2,
                repeat: Infinity,
                ease: "linear",
              }}
            >
              <motion.div
                className="w-2 h-2 rounded-full bg-primary glow-cyan"
                style={{
                  transform: `translateX(${60 + i * 15}px)`,
                }}
                animate={{
                  opacity: [0.3, 1, 0.3],
                  scale: [0.8, 1.2, 0.8],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  delay: i * 0.3,
                }}
              />
            </motion.div>
          ))}
        </motion.div>
      </motion.div>

      {/* Title */}
      <motion.div
        className="relative z-10 text-center px-4"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.3 }}
      >
        <h1 className="font-display text-4xl md:text-6xl lg:text-7xl font-bold tracking-wider mb-4">
          <span className="text-glow-cyan text-primary">NEURO</span>
          <span className="text-foreground">SENSE</span>
        </h1>
        
        <motion.div
          className="h-[2px] w-48 md:w-64 mx-auto my-6 bg-gradient-to-r from-transparent via-primary to-transparent"
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
        />

        <h2 className="font-display text-lg md:text-xl lg:text-2xl text-primary/80 tracking-widest mb-4">
          EEG EMOTION INTELLIGENCE
        </h2>

        <p className="font-body text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto">
          Upload EEG → Analyze Valence → Predict Emotional State
        </p>

        {/* System Status */}
        <motion.div
          className="mt-8 system-notification inline-block"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
        >
          <span className="text-primary mr-2">◈</span>
          SYSTEM ONLINE — NEURAL ANALYSIS READY
          <span className="text-primary ml-2">◈</span>
        </motion.div>
      </motion.div>

      {/* Floating Particles */}
      <div className="particles">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="particle"
            style={{
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
            }}
            animate={{
              y: [100, -100],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: 3 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </div>
    </section>
  );
};

export default HeroSection;
