import { useState, useEffect } from 'react';

function Display (props) {

    const [text, setText] = useState("Loading...")

    useEffect(() => {
        setTimeout(() => {
            setText(`カウント: ${props.count}`)
        }, 1000)
    }, [])

    return (
        <>
            {text}
        </>
    )
}

export default Display