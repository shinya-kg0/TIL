import { useLocation, Link } from "react-router-dom"
import { ROUTES } from "../const";
import Result from "../components/Result/Result";
import Confetti from 'react-confetti';
import Loading from "../components/Loading/Loading";
import { useState, useEffect } from "react";

export default function ResultPage() {
    const [active, setActive] = useState(false);
    const location = useLocation();
    const maxQuizLen = location.state.maxQuizLen;
    const correctNumLen = location.state.correctNumLen;

    useEffect(() => {
        setTimeout(() => setActive(true), 1500)
    }, [])

    return (
        <>
            <Loading active={active} />
            <h1>Result</h1>
            <Result maxQuizLen={maxQuizLen} correctNumLen={correctNumLen} />
            <br />

            <Link to={ROUTES.QUIZ}>もう一度チャレンジする！</Link>
            <br />
            <Link to={ROUTES.HOME}>ホームへ戻る</Link>

            <Confetti />
        </>
    )
}
