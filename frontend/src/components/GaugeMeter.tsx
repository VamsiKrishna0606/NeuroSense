import { motion } from "framer-motion";

interface GaugeMeterProps {
  value: number; // 0 to 1
  isHigh: boolean;
}

const GaugeMeter = ({ value, isHigh }: GaugeMeterProps) => {
  const radius = 80;
  const strokeWidth = 12;
  const normalizedRadius = radius - strokeWidth / 2;
  const circumference = normalizedRadius * Math.PI; // Semi-circle
  const strokeDashoffset = circumference - value * circumference;

  return (
    <div className="relative">
      <svg
        height={radius + 20}
        width={radius * 2 + 20}
        className="transform -rotate-180"
        style={{ transform: "rotate(-90deg)" }}
      >
        {/* Background Arc */}
        <circle
          stroke="hsl(var(--muted))"
          fill="transparent"
          strokeWidth={strokeWidth}
          r={normalizedRadius}
          cx={radius + 10}
          cy={radius + 10}
          strokeDasharray={`${circumference} ${circumference}`}
          strokeLinecap="round"
        />
        
        {/* Gradient Definition */}
        <defs>
          <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop 
              offset="0%" 
              stopColor={isHigh ? "hsl(var(--glow-purple))" : "hsl(var(--destructive))"} 
            />
            <stop 
              offset="100%" 
              stopColor={isHigh ? "hsl(var(--glow-cyan))" : "hsl(var(--glow-pink))"} 
            />
          </linearGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        {/* Animated Progress Arc */}
        <motion.circle
          stroke="url(#gaugeGradient)"
          fill="transparent"
          strokeWidth={strokeWidth}
          r={normalizedRadius}
          cx={radius + 10}
          cy={radius + 10}
          strokeDasharray={`${circumference} ${circumference}`}
          strokeLinecap="round"
          filter="url(#glow)"
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.5, ease: "easeOut" }}
        />

        {/* Tick Marks */}
        {[...Array(11)].map((_, i) => {
          const angle = (i / 10) * 180;
          const innerRadius = normalizedRadius - 20;
          const outerRadius = normalizedRadius - 15;
          const x1 = radius + 10 + innerRadius * Math.cos((angle * Math.PI) / 180);
          const y1 = radius + 10 + innerRadius * Math.sin((angle * Math.PI) / 180);
          const x2 = radius + 10 + outerRadius * Math.cos((angle * Math.PI) / 180);
          const y2 = radius + 10 + outerRadius * Math.sin((angle * Math.PI) / 180);
          
          return (
            <line
              key={i}
              x1={x1}
              y1={y1}
              x2={x2}
              y2={y2}
              stroke="hsl(var(--muted-foreground))"
              strokeWidth={i % 5 === 0 ? 2 : 1}
              opacity={0.5}
            />
          );
        })}
      </svg>

      {/* Center Display */}
      <div className="absolute inset-0 flex items-end justify-center pb-2">
        <div className="text-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.5, type: "spring" }}
            className={`
              w-8 h-8 mx-auto mb-2 rounded-full flex items-center justify-center
              ${isHigh ? "bg-accent/20 border border-accent/50" : "bg-destructive/20 border border-destructive/50"}
            `}
          >
            <motion.div
              className={`w-3 h-3 rounded-full ${isHigh ? "bg-accent" : "bg-destructive"}`}
              animate={{
                scale: [1, 1.3, 1],
                opacity: [0.8, 1, 0.8],
              }}
              transition={{ duration: 1.5, repeat: Infinity }}
            />
          </motion.div>
        </div>
      </div>

      {/* Labels */}
      <div className="absolute -bottom-2 left-0 right-0 flex justify-between px-2">
        <span className="font-display text-xs text-muted-foreground">0%</span>
        <span className="font-display text-xs text-muted-foreground">100%</span>
      </div>
    </div>
  );
};

export default GaugeMeter;
