import { useState, useEffect } from "react";
// import "../App.css";

const API_BASE = "http://localhost:5000";

const MORNING_SLOTS   = ["09:00","09:30","10:00","10:30","11:00","11:30","12:00","12:30"];
const AFTERNOON_SLOTS = ["15:00","15:30","16:00","16:30","17:00","17:30"];
const ALL_SLOTS       = [...MORNING_SLOTS, ...AFTERNOON_SLOTS];

const DAYS_IT   = ["Lun","Mar","Mer","Gio","Ven","Sab","Dom"];
const MONTHS_IT = ["Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno",
                   "Luglio","Agosto","Settembre","Ottobre","Novembre","Dicembre"];

function toDateStr(y, m, d) {
  return `${y}-${String(m + 1).padStart(2,"0")}-${String(d).padStart(2,"0")}`;
}

export default function AppointmentForm({ pazienteId = 1, onSuccess }) {
  const today = new Date(); today.setHours(0, 0, 0, 0);

  const [medici,         setMedici]         = useState([]);
  const [selectedMedico, setSelectedMedico] = useState(null);
  const [occupati,       setOccupati]       = useState([]);
  const [calYear,        setCalYear]        = useState(today.getFullYear());
  const [calMonth,       setCalMonth]       = useState(today.getMonth());
  const [selectedDate,   setSelectedDate]   = useState(null);
  const [selectedSlot,   setSelectedSlot]   = useState(null);
  const [note,           setNote]           = useState("");
  const [loading,        setLoading]        = useState(false);
  const [error,          setError]          = useState(null);
  const [success,        setSuccess]        = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/appuntamenti/medici`)
      .then(r => r.json())
      .then(setMedici)
      .catch(() => setError("Impossibile caricare i medici."));
  }, []);

  useEffect(() => {
    if (!selectedMedico) return;
    const from = toDateStr(calYear, calMonth, 1);
    const lastDay = new Date(calYear, calMonth + 1, 0).getDate();
    const to = toDateStr(calYear, calMonth, lastDay);
    fetch(`${API_BASE}/appuntamenti/medici/${selectedMedico.id}/slot-occupati?from=${from}&to=${to}`)
      .then(r => r.json())
      .then(setOccupati)
      .catch(() => setOccupati([]));
  }, [selectedMedico, calYear, calMonth]);

  function getAvailableDays() {
    const days = new Set();
    const daysInMonth = new Date(calYear, calMonth + 1, 0).getDate();
    for (let d = 1; d <= daysInMonth; d++) {
      const date = new Date(calYear, calMonth, d);
      if (date < today) continue;
      if (date.getDay() === 0 || date.getDay() === 6) continue;
      const dateStr = toDateStr(calYear, calMonth, d);
      const hasFree = ALL_SLOTS.some(t => !occupati.includes(`${dateStr} ${t}`));
      if (hasFree) days.add(d);
    }
    return days;
  }

  function onMedicoChange(e) {
    const m = medici.find(x => x.id === parseInt(e.target.value)) || null;
    setSelectedMedico(m);
    setSelectedDate(null);
    setSelectedSlot(null);
  }

  function prevMonth() {
    if (calMonth === 0) { setCalMonth(11); setCalYear(y => y - 1); }
    else setCalMonth(m => m - 1);
    setSelectedDate(null); setSelectedSlot(null);
  }

  function nextMonth() {
    if (calMonth === 11) { setCalMonth(0); setCalYear(y => y + 1); }
    else setCalMonth(m => m + 1);
    setSelectedDate(null); setSelectedSlot(null);
  }

  function selectDate(dateStr) {
    setSelectedDate(dateStr);
    setSelectedSlot(null);
  }

  async function handleSubmit() {
    if (!selectedMedico || !selectedDate || !selectedSlot) return;
    setLoading(true); setError(null);
    try {
      const res = await fetch(`${API_BASE}/appuntamenti`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          medico_id:     selectedMedico.id,
          paziente_id:   pazienteId,
          data_ora:      `${selectedDate} ${selectedSlot}`,
          durata_minuti: 30,
          note
        })
      });
      if (res.status === 409) { setError("Slot già occupato, scegli un altro orario."); return; }
      if (!res.ok) throw new Error();
      setSuccess(true);
      onSuccess?.();
    } catch {
      setError("Errore durante la prenotazione. Riprova.");
    } finally {
      setLoading(false);
    }
  }

  if (success) {
    return (
      <div className="card">
        <div className="success-box">
          <div className="success-icon">✓</div>
          <div className="success-title">Appuntamento confermato</div>
          <div className="success-detail">
            {selectedMedico?.nome} — {selectedDate} alle {selectedSlot}
          </div>
          <button className="reset-btn" onClick={() => {
            setSuccess(false); setSelectedMedico(null);
            setSelectedDate(null); setSelectedSlot(null); setNote("");
          }}>
            Prenota un altro
          </button>
        </div>
      </div>
    );
  }

  const availDays   = getAvailableDays();
  const daysInMonth = new Date(calYear, calMonth + 1, 0).getDate();
  let   startDow    = new Date(calYear, calMonth, 1).getDay();
  startDow          = startDow === 0 ? 6 : startDow - 1;

  return (
    <div className="card">
      <h4 className="title">Prenota appuntamento</h4>

      {/* Selezione medico */}
      <div className="field">
        <label className="label">Medico</label>
        <select className="select" onChange={onMedicoChange} value={selectedMedico?.id || ""}>
          <option value="">Seleziona un medico...</option>
          {medici.map(m => (
            <option key={m.id} value={m.id}>
              {m.nome} — {m.specializzazione}
            </option>
          ))}
        </select>
      </div>

      {/* Calendario */}
      {selectedMedico && (
        <div className="field">
          <label className="label">Data</label>
          <div className="cal-wrap">
            <div className="cal-header">
              <button className="nav-btn" onClick={prevMonth}>‹</button>
              <span className="cal-month">{MONTHS_IT[calMonth]} {calYear}</span>
              <button className="nav-btn" onClick={nextMonth}>›</button>
            </div>
            <div className="cal-grid">
              {DAYS_IT.map(d => (
                <div key={d} className="day-label">{d}</div>
              ))}
              {Array.from({ length: startDow }).map((_, i) => (
                <div key={`blank-${i}`} />
              ))}
              {Array.from({ length: daysInMonth }, (_, i) => i + 1).map(d => {
                const date    = new Date(calYear, calMonth, d);
                const dateStr = toDateStr(calYear, calMonth, d);
                const isPast  = date < today;
                const isAvail = availDays.has(d);
                const isSel   = selectedDate === dateStr;
                const isToday = date.toDateString() === today.toDateString();

                let cls = "day-cell";
                if (isPast)       cls += " day-cell-past";
                else if (isSel)   cls += " day-cell-selected";
                else if (isAvail) cls += " day-cell-avail";
                if (isToday && !isSel) cls += " today";

                return (
                  <div
                    key={d}
                    className={cls}
                    style={isToday && !isSel ? { fontWeight: 600 } : undefined}
                    onClick={() => isAvail && !isPast && selectDate(dateStr)}
                  >
                    {d}
                  </div>
                );
              })}
            </div>
          </div>
          <div className="legend">
            <span className="legend-dot" />
            <span className="legend-text">Disponibile</span>
          </div>
        </div>
      )}

      {/* Slot orari */}
      {selectedDate && (
        <div className="field">
          <label className="label">Orario</label>
          <div className="slot-section">
            <div className="slot-group-label">Mattina</div>
            <div className="slot-grid">
              {MORNING_SLOTS.map(t => {
                const occ = occupati.includes(`${selectedDate} ${t}`);
                const sel = selectedSlot === t;
                let cls = "slot-btn";
                if (occ) cls += " slot-occ";
                if (sel) cls += " slot-sel";
                return (
                  <button key={t} className={cls} disabled={occ}
                    onClick={() => !occ && setSelectedSlot(t)}>
                    {t}
                  </button>
                );
              })}
            </div>
            <div className="slot-group-label" style={{ marginTop: 8 }}>Pomeriggio</div>
            <div className="slot-grid">
              {AFTERNOON_SLOTS.map(t => {
                const occ = occupati.includes(`${selectedDate} ${t}`);
                const sel = selectedSlot === t;
                let cls = "slot-btn";
                if (occ) cls += " slot-occ";
                if (sel) cls += " slot-sel";
                return (
                  <button key={t} className={cls} disabled={occ}
                    onClick={() => !occ && setSelectedSlot(t)}>
                    {t}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Note */}
      {selectedMedico && (
        <div className="field">
          <label className="label">Note</label>
          <textarea
            className="textarea"
            placeholder="Informazioni aggiuntive..."
            value={note}
            onChange={e => setNote(e.target.value)}
          />
        </div>
      )}

      {error && <div className="error-box">{error}</div>}

      <button
        className="confirm-btn"
        style={{ opacity: (!selectedMedico || !selectedDate || !selectedSlot || loading) ? 0.45 : 1 }}
        disabled={!selectedMedico || !selectedDate || !selectedSlot || loading}
        onClick={handleSubmit}
      >
        {loading ? "Prenotazione in corso..." : "Conferma appuntamento"}
      </button>
    </div>
  );
}