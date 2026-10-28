import {
  Bar, BarChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart,
  ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts'

const OLIVE = { primary: '#68734A', accent: '#8D9B68', forest: '#35452F', pos: '#5a7a3f', neg: '#b4552f', neu: '#a79a5e', grid: '#E3E3D8' }

export function SentimentPie({ distribution }) {
  const data = [
    { name: 'Positive', value: distribution.positive, color: OLIVE.pos },
    { name: 'Neutral', value: distribution.neutral, color: OLIVE.neu },
    { name: 'Negative', value: distribution.negative, color: OLIVE.neg },
  ].filter((d) => d.value > 0)
  return (
    <ResponsiveContainer width="100%" height={240}>
      <PieChart>
        <Pie data={data} dataKey="value" nameKey="name" innerRadius={55} outerRadius={85} paddingAngle={2}>
          {data.map((d) => <Cell key={d.name} fill={d.color} />)}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  )
}

export function AspectBars({ aspects }) {
  const data = aspects.slice(0, 10).map((a) => ({ aspect: a.aspect, score: a.score, total: a.total }))
  return (
    <ResponsiveContainer width="100%" height={Math.max(240, data.length * 34)}>
      <BarChart data={data} layout="vertical" margin={{ left: 20, right: 20 }}>
        <CartesianGrid stroke={OLIVE.grid} horizontal={false} />
        <XAxis type="number" domain={[-1, 1]} stroke={OLIVE.forest} fontSize={12} />
        <YAxis type="category" dataKey="aspect" width={90} stroke={OLIVE.forest} fontSize={12} />
        <Tooltip formatter={(v, n) => n === 'score' ? [v, 'sentiment score'] : [v, n]} />
        <Bar dataKey="score" radius={[0, 4, 4, 0]}>
          {data.map((d) => <Cell key={d.aspect} fill={d.score >= 0.3 ? OLIVE.pos : d.score <= -0.3 ? OLIVE.neg : OLIVE.neu} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}

export function TrendLines({ points }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={points} margin={{ left: 0, right: 12 }}>
        <CartesianGrid stroke={OLIVE.grid} />
        <XAxis dataKey="month" stroke={OLIVE.forest} fontSize={11} />
        <YAxis stroke={OLIVE.forest} fontSize={11} />
        <Tooltip />
        <Line type="monotone" dataKey="avg_rating" name="Avg rating" stroke={OLIVE.primary} strokeWidth={2} dot={false} />
        <Line type="monotone" dataKey="positive_share" name="Positive share" stroke={OLIVE.accent} strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  )
}

export function VolumeTrend({ points }) {
  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={points} margin={{ left: 0, right: 12 }}>
        <CartesianGrid stroke={OLIVE.grid} vertical={false} />
        <XAxis dataKey="month" stroke={OLIVE.forest} fontSize={11} />
        <YAxis stroke={OLIVE.forest} fontSize={11} allowDecimals={false} />
        <Tooltip />
        <Bar dataKey="review_count" name="Reviews" fill={OLIVE.accent} radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}

export function PriceLine({ history }) {
  return (
    <ResponsiveContainer width="100%" height={240}>
      <LineChart data={history} margin={{ left: 0, right: 12 }}>
        <CartesianGrid stroke={OLIVE.grid} />
        <XAxis dataKey="date" stroke={OLIVE.forest} fontSize={11} />
        <YAxis stroke={OLIVE.forest} fontSize={11} domain={['auto', 'auto']} />
        <Tooltip formatter={(v) => [`$${v}`, 'price']} />
        <Line type="monotone" dataKey="price" stroke={OLIVE.primary} strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  )
}
