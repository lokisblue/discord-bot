// status can be "online", "idle", "dnd", or "invisible" or "offline"
export default [
    {
        channelId: "1304951669309833300",
        serverId: "1304951669309833296",
        token: process.env.token1,
        selfDeaf: false,
        autoReconnect: {
            enabled: true,
            delay: 5, // ثواني
            maxRetries: 5,
        },
        presence: {
            status: "idle",
        },
        selfMute: true,
    },
];
