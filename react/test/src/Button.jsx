function Button(props) {

    const { type, disabled, children, onClick} = props;

    // const handleClick = () => {
    //     alert("クリックされました！")
    // }

    return (
        <button type={type} disabled={disabled} onClick={onClick}>
            {children}
        </button>
    )
}

export default Button;
