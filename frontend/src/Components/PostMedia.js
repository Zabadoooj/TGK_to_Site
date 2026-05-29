import "./PostMedia.css"

// components/PostMedia.jsx
const API = "http://localhost:8000";

export default function PostMedia({ media }) {
    if (!media || media.type === "none") return null;

    // Фото — грузим через наш прокси эндпоинт
    if (media.type === "photo" || media.type === "animation") {
    return (
        <img
            src={media.url}
            alt="Фото"
            style={{ maxWidth: "100%", borderRadius: 8 }}
        />
    );
}

    // GIF-анимация
    if (media.type === "animation") {
        return (
            <img
                src={`${API}/photo/${media.file_id}`}
                alt="GIF"
                style={{ maxWidth: "100%", borderRadius: 8 }}
            />
        );
    }

    // Всё остальное — текстовая плашка
    const icons = {
        audio:      "🎵",
        voice:      "🎙",
        video:      "🎬",
        video_note: "📹",
        document:   "📎",
        sticker:    "🎭",
    };

    const icon = icons[media.type] || "📎";
    const label = media.label || media.type;

    return (
        <div className="Post" style={{
            background: "#f0f0f0",
            borderRadius: 8,
            padding: "8px 12px",
            display: "inline-block",
            color: "#555",
            fontSize: 14
        }}>
            {icon} {label}
        </div>
    );
}