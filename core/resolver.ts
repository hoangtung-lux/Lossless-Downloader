// Lumina Music - Spotify Resolver Core (Deno/TypeScript)
// Handles ISRC and GraphQL Resolution with High Performance

const SPOTIFY_GRAPHQL_ENDPOINT = "https://api-partner.spotify.com/pathfinder/v1/query";
const SHA256_HASH = "612585ae06ba435ad26369870deaae23b5c8800a256cd8a57e08eddc25a37294";

async function getSpotifyToken() {
    const res = await fetch("https://open.spotify.com/get_access_token?reason=transport&productType=web_player", {
        headers: {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    });
    if (!res.ok) throw new Error("Failed to get Spotify token: " + res.status);
    const data = await res.json();
    return data.accessToken;
}

async function resolveTrack(trackId: string) {
    const token = await getSpotifyToken();
    const variables = {
        uri: `spotify:track:${trackId}`
    };
    
    const url = `${SPOTIFY_GRAPHQL_ENDPOINT}?operationName=getTrack&variables=${encodeURIComponent(JSON.stringify(variables))}&extensions=${encodeURIComponent(JSON.stringify({persistedQuery: {sha256Hash: SHA256_HASH}}))}`;

    const res = await fetch(url, {
        headers: {
            "Authorization": `Bearer ${token}`,
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
        }
    });

    const data = await res.json();
    const track = data.data.trackUnion;
    
    return {
        id: track.id,
        name: track.name,
        isrc: track.externalIds.items[0]?.value,
        artist: track.firstArtist.items[0]?.profile.name,
        album: track.album.name,
        cover: track.album.coverArt.sources[0]?.url
    };
}

// Main CLI Entry
const args = Deno.args;
if (args.length > 0) {
    const trackId = args[0];
    try {
        const result = await resolveTrack(trackId);
        console.log(JSON.stringify(result));
    } catch (e) {
        console.error(JSON.stringify({error: e.message}));
    }
}
