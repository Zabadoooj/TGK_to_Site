import PostMedia from "./PostMedia";
import { useTelegramMessages } from "../Hooks/useTelegramMessages";

import './PostList.css'
import config from "../_config";


export default function PostList() {

    const messages_arr = []

    for (let i = config.from_msg; i <= config.to_msg; i++){
        messages_arr.push(i)
    }

    const { messages, loading, error } = useTelegramMessages(messages_arr);

    

    if (loading) return <div className="loading">Загрузка...</div>;
    if (error) return <div className="error">Ошибка!</div>;

    return (
        <div className="PostsList">
            {messages.map((msg) => (
                <article className="PostItem" key={msg.id}>
                    <PostMedia media={msg.media} />
                    {msg.text && <div className="Title">{msg.text}</div>}
                    <div className="DateTime">
                        <div className="Date">{new Date(msg.date).toLocaleDateString("ru-RU")}</div>
                        <div className="Time">{new Date(msg.date).toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" })}</div>
                    </div>
                </article>
            ))}
        </div>
    );
}