import { motion } from "framer-motion";
import { useState } from "react";

interface BandData {
  name: string;
  value: number;
  color: string;
  description: string;
  frequency: string;
}

interface BandContributionProps {
  bands: BandData[];
}

const BandContribution = ({ bands }: BandContributionProps) => {
  const [hoveredBand, setHoveredBand] = useState<string | null>(null);

  if (bands.length === 0) return null;

  return (
    <section className="py-12 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-4xl mx-auto"
      >
        {/* Section Header */}
        <div className="text-center mb-8">
          <h3 className="font-display text-2xl md:text-3xl text-primary text-glow-cyan mb-2">
            BAND CONTRIBUTION ANALYSIS
          </h3>
          <p className="font-body text-muted-foreground">
            Neural frequency band power distribution
          </p>
        </div>

        {/* Bands Container */}
        <div className="glass-panel p-6 md:p-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {bands.map((band, index) => (
              <motion.div
                key={band.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="relative"
                onMouseEnter={() => setHoveredBand(band.name)}
                onMouseLeave={() => setHoveredBand(null)}
              >
                {/* Vertical Bar Container */}
                <div className="relative h-48 flex flex-col items-center">
                  {/* Bar Background */}
                  <div className="relative w-12 h-full bg-muted/50 rounded-full overflow-hidden">
                    {/* Animated Fill */}
                    <motion.div
                      className="absolute bottom-0 left-0 right-0 rounded-full"
                      style={{
                        background: `linear-gradient(to top, ${band.color}80, ${band.color})`,
                        boxShadow: `0 0 20px ${band.color}60`,
                      }}
                      initial={{ height: "0%" }}
                      animate={{ height: `${band.value * 100}%` }}
                      transition={{ duration: 1, delay: 0.3 + index * 0.1, ease: "easeOut" }}
                    />

                    {/* Glow Effect on Hover */}
                    <motion.div
                      className="absolute inset-0 rounded-full"
                      animate={{
                        boxShadow: hoveredBand === band.name
                          ? `0 0 30px ${band.color}80, inset 0 0 20px ${band.color}40`
                          : "none",
                      }}
                    />

                    {/* Animated Particles Inside Bar */}
                    {hoveredBand === band.name && (
                      <>
                        {[...Array(5)].map((_, i) => (
                          <motion.div
                            key={i}
                            className="absolute w-1 h-1 rounded-full"
                            style={{
                              background: band.color,
                              left: `${20 + Math.random() * 60}%`,
                            }}
                            animate={{
                              bottom: ["0%", `${band.value * 100}%`],
                              opacity: [0, 1, 0],
                            }}
                            transition={{
                              duration: 1 + Math.random(),
                              repeat: Infinity,
                              delay: Math.random() * 0.5,
                            }}
                          />
                        ))}
                      </>
                    )}
                  </div>

                  {/* Value Display */}
                  <motion.div
                    className="mt-3 text-center"
                    animate={{
                      scale: hoveredBand === band.name ? 1.1 : 1,
                    }}
                  >
                    <p
                      className="font-display text-2xl font-bold"
                      style={{ color: band.color }}
                    >
                      {(band.value * 100).toFixed(0)}%
                    </p>
                  </motion.div>
                </div>

                {/* Band Label */}
                <div className="mt-4 text-center">
                  <p
                    className="font-display text-lg tracking-wider"
                    style={{ color: band.color }}
                  >
                    {band.name.toUpperCase()}
                  </p>
                  <p className="font-body text-xs text-muted-foreground mt-1">
                    {band.frequency}
                  </p>
                </div>

                {/* Tooltip */}
                <motion.div
                  className="absolute -top-24 left-1/2 -translate-x-1/2 w-48 z-20"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{
                    opacity: hoveredBand === band.name ? 1 : 0,
                    y: hoveredBand === band.name ? 0 : 10,
                  }}
                  transition={{ duration: 0.2 }}
                  style={{ pointerEvents: "none" }}
                >
                  <div
                    className="glass-panel p-3 text-center"
                    style={{
                      borderColor: `${band.color}50`,
                      boxShadow: `0 0 20px ${band.color}30`,
                    }}
                  >
                    <p className="font-body text-sm text-foreground">
                      {band.description}
                    </p>
                  </div>
                  {/* Arrow */}
                  <div
                    className="w-3 h-3 mx-auto -mt-1.5 rotate-45"
                    style={{
                      background: "hsl(var(--glass))",
                      borderRight: `1px solid ${band.color}50`,
                      borderBottom: `1px solid ${band.color}50`,
                    }}
                  />
                </motion.div>
              </motion.div>
            ))}
          </div>

          {/* Legend */}
          <div className="mt-8 pt-6 border-t border-border/50">
            <div className="flex flex-wrap justify-center gap-4">
              {bands.map((band) => (
                <div key={band.name} className="flex items-center gap-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{
                      background: band.color,
                      boxShadow: `0 0 10px ${band.color}80`,
                    }}
                  />
                  <span className="font-body text-sm text-muted-foreground">
                    {band.name}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </motion.div>
    </section>
  );
};

export default BandContribution;
