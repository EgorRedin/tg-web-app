const tg = window.Telegram.WebApp;

export function useTelegram()
{
    const onClose = () =>
    {
        tg.close()
    }

    return {
        onClose,
        tg,
        userTg: tg.initDataUnsafe?.user, 
    }
}