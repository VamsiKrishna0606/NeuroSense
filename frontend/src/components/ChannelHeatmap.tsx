import { motion } from "framer-motion";
import { useState } from "react";

interface ChannelData {
  id: string;
  name: string;
  value: number; // 0 to 1
  x: number; // Grid position
  y: number;
}

interface ChannelHeatmapProps {
  channels: ChannelData[];
}

// Standard 10-20 system electrode positions (approximate grid layout)
const defaultChannels: ChannelData[] = [
  // Row 1 (top)
  { id: "1", name: "Fp1", value: 0.6, x: 2, y: 0 },
  { id: "2", name: "Fpz", value: 0.55, x: 3, y: 0 },
  { id: "3", name: "Fp2", value: 0.65, x: 4, y: 0 },
  // Row 2
  { id: "4", name: "AF7", value: 0.45, x: 1, y: 1 },
  { id: "5", name: "AF3", value: 0.5, x: 2, y: 1 },
  { id: "6", name: "AFz", value: 0.52, x: 3, y: 1 },
  { id: "7", name: "AF4", value: 0.48, x: 4, y: 1 },
  { id: "8", name: "AF8", value: 0.42, x: 5, y: 1 },
  // Row 3
  { id: "9", name: "F7", value: 0.7, x: 0, y: 2 },
  { id: "10", name: "F5", value: 0.68, x: 1, y: 2 },
  { id: "11", name: "F3", value: 0.72, x: 2, y: 2 },
  { id: "12", name: "Fz", value: 0.75, x: 3, y: 2 },
  { id: "13", name: "F4", value: 0.73, x: 4, y: 2 },
  { id: "14", name: "F6", value: 0.69, x: 5, y: 2 },
  { id: "15", name: "F8", value: 0.71, x: 6, y: 2 },
  // Row 4
  { id: "16", name: "T7", value: 0.4, x: 0, y: 3 },
  { id: "17", name: "C5", value: 0.55, x: 1, y: 3 },
  { id: "18", name: "C3", value: 0.6, x: 2, y: 3 },
  { id: "19", name: "Cz", value: 0.65, x: 3, y: 3 },
  { id: "20", name: "C4", value: 0.62, x: 4, y: 3 },
  { id: "21", name: "C6", value: 0.58, x: 5, y: 3 },
  { id: "22", name: "T8", value: 0.38, x: 6, y: 3 },
  // Row 5
  { id: "23", name: "P7", value: 0.8, x: 0, y: 4 },
  { id: "24", name: "P5", value: 0.78, x: 1, y: 4 },
  { id: "25", name: "P3", value: 0.82, x: 2, y: 4 },
  { id: "26", name: "Pz", value: 0.85, x: 3, y: 4 },
  { id: "27", name: "P4", value: 0.83, x: 4, y: 4 },
  { id: "28", name: "P6", value: 0.79, x: 5, y: 4 },
  { id: "29", name: "P8", value: 0.77, x: 6, y: 4 },
  // Row 6 (bottom)
  { id: "30", name: "O1", value: 0.9, x: 2, y: 5 },
  { id: "31", name: "Oz", value: 0.92, x: 3, y: 5 },
  { id: "32", name: "O2", value: 0.88, x: 4, y: 5 },
];

const getHeatColor = (value: number) => {
  // Cold to hot gradient (blue -> cyan -> green -> yellow -> orange -> red)
  if (value < 0.2) return `hsl(220, 80%, ${30 + value * 100}%)`;
  if (value < 0.4) return `hsl(195, 90%, ${40 + value * 50}%)`;
  if (value < 0.6) return `hsl(160, 80%, ${45 + value * 30}%)`;
  if (value < 0.8) return `hsl(45, 90%, ${50 + value * 20}%)`;
  return `hsl(0, 80%, ${50 + value * 20}%)`;
};

const ChannelHeatmap = ({ channels = defaultChannels }: ChannelHeatmapProps) => {
  const [hoveredChannel, setHoveredChannel] = useState<ChannelData | null>(null);

  return (
    <section className="py-12 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-3xl mx-auto"
      >
        {/* Section Header */}
        <div className="text-center mb-8">
          <h3 className="font-display text-2xl md:text-3xl text-primary text-glow-cyan mb-2">
            CHANNEL ACTIVATION MAP
          </h3>
          <p className="font-body text-muted-foreground">
            Neural signal intensity across 32 electrode positions
          </p>
        </div>

        {/* Heatmap Container */}
        <div className="glass-panel p-6 md:p-8">
          {/* Brain Outline */}
          <div className="relative max-w-md mx-auto">
            {/* Brain Shape Background */}
            <svg
              viewBox="0 0 200 200"
              className="absolute inset-0 w-full h-full opacity-20"
            >
              <ellipse
                cx="100"
                cy="100"
                rx="90"
                ry="95"
                fill="none"
                stroke="hsl(var(--primary))"
                strokeWidth="2"
              />
              {/* Nose indicator */}
              <polygon
                points="100,5 95,20 105,20"
                fill="hsl(var(--primary))"
                opacity="0.5"
              />
            </svg>

            {/* Grid Container */}
            <div
              className="relative grid gap-2 p-8"
              style={{
                gridTemplateColumns: "repeat(7, 1fr)",
                gridTemplateRows: "repeat(6, 1fr)",
              }}
            >
              {/* Empty cells for positioning */}
              {[...Array(42)].map((_, i) => {
                const x = i % 7;
                const y = Math.floor(i / 7);
                const channel = channels.find((c) => c.x === x && c.y === y);

                if (!channel) {
                  return <div key={i} className="aspect-square" />;
                }

                return (
                  <motion.div
                    key={channel.id}
                    initial={{ scale: 0, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{
                      delay: parseInt(channel.id) * 0.03,
                      type: "spring",
                    }}
                    className="aspect-square relative"
                    onMouseEnter={() => setHoveredChannel(channel)}
                    onMouseLeave={() => setHoveredChannel(null)}
                  >
                    <motion.div
                      className="w-full h-full rounded-lg cursor-pointer flex items-center justify-center relative overflow-hidden"
                      style={{
                        background: getHeatColor(channel.value),
                        boxShadow:
                          hoveredChannel?.id === channel.id
                            ? `0 0 20px ${getHeatColor(channel.value)}, 0 0 40px ${getHeatColor(channel.value)}80`
                            : `0 0 10px ${getHeatColor(channel.value)}60`,
                      }}
                      whileHover={{ scale: 1.15, zIndex: 10 }}
                      animate={{
                        opacity: [0.8, 1, 0.8],
                      }}
                      transition={{
                        opacity: {
                          duration: 2 + Math.random(),
                          repeat: Infinity,
                          delay: Math.random(),
                        },
                      }}
                    >
                      {/* Channel Name */}
                      <span className="font-display text-[10px] text-background font-bold">
                        {channel.name}
                      </span>

                      {/* Pulse Effect */}
                      {channel.value > 0.7 && (
                        <motion.div
                          className="absolute inset-0 rounded-lg"
                          style={{
                            border: `2px solid ${getHeatColor(channel.value)}`,
                          }}
                          animate={{
                            scale: [1, 1.3, 1],
                            opacity: [0.5, 0, 0.5],
                          }}
                          transition={{
                            duration: 1.5,
                            repeat: Infinity,
                          }}
                        />
                      )}
                    </motion.div>
                  </motion.div>
                );
              })}
            </div>

            {/* Tooltip */}
            {hoveredChannel && (
              <motion.div
                className="absolute top-4 right-4 glass-panel p-4 z-20"
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
              >
                <p className="font-display text-primary text-lg">
                  {hoveredChannel.name}
                </p>
                <p className="font-body text-sm text-muted-foreground">
                  Channel #{hoveredChannel.id}
                </p>
                <div className="mt-2 flex items-center gap-2">
                  <div
                    className="w-4 h-4 rounded"
                    style={{ background: getHeatColor(hoveredChannel.value) }}
                  />
                  <span className="font-display text-foreground">
                    {(hoveredChannel.value * 100).toFixed(0)}%
                  </span>
                </div>
              </motion.div>
            )}
          </div>

          {/* Color Legend */}
          <div className="mt-8 pt-6 border-t border-border/50">
            <p className="font-display text-sm text-muted-foreground text-center mb-4">
              SIGNAL INTENSITY
            </p>
            <div className="flex justify-center items-center gap-2">
              <span className="font-body text-xs text-muted-foreground">LOW</span>
              <div
                className="h-4 w-48 rounded-full"
                style={{
                  background:
                    "linear-gradient(to right, hsl(220 80% 40%), hsl(195 90% 50%), hsl(160 80% 50%), hsl(45 90% 55%), hsl(0 80% 55%))",
                }}
              />
              <span className="font-body text-xs text-muted-foreground">HIGH</span>
            </div>
          </div>
        </div>
      </motion.div>
    </section>
  );
};

export default ChannelHeatmap;
