<template>
  <div class="Lumina Music-showcase min-h-screen bg-[#121212] text-white font-sans selection:bg-[#1DB954] selection:text-black">
    <!-- Navigation -->
    <nav class="sticky top-0 z-50 bg-[#000000]/80 backdrop-blur-md border-b border-[#282828] p-4 flex justify-between items-center px-6 md:px-12">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-[#1DB954] rounded-full flex items-center justify-center shadow-[0_0_15px_rgba(29,185,84,0.5)]">
          <svg viewBox="0 0 24 24" class="w-5 h-5 fill-black" xmlns="http://www.w3.org/2000/svg"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg>
        </div>
        <span class="font-bold text-xl tracking-tight hidden sm:block">Lumina Music Clone</span>
      </div>
      <a href="/" class="text-[#b3b3b3] hover:text-white transition-colors flex items-center gap-2 text-sm font-medium">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
        Quay lại VIBE
      </a>
    </nav>

    <!-- Hero Section -->
    <section class="max-w-6xl mx-auto pt-16 pb-12 px-6 text-center lg:text-left lg:flex lg:items-center lg:gap-12">
      <div class="lg:w-1/2 space-y-6">
        <h1 class="text-4xl md:text-6xl font-extrabold leading-tight tracking-tighter animate-fade-in">
          Tải Nhạc <span class="text-[#1DB954] drop-shadow-[0_0_10px_rgba(29,185,84,0.3)]">Lossless</span> <br/>
          Thật Sự Theo Cách <br/>
          Của Bạn.
        </h1>
        <p class="text-[#b3b3b3] text-lg max-w-lg mx-auto lg:mx-0 leading-relaxed">
          Trình tải nhạc tối ưu hỗ trợ Hi-Fi thực sự từ Tidal, Deezer & Qobuz. 
          Giao diện Spotify mượt mà, tốc độ siêu tốc với 16 luồng tải song song.
        </p>
        <div class="flex flex-wrap justify-center lg:justify-start gap-4">
          <a href="https://github.com/hoangtung-lux/Lossless-Downloader/releases" target="_blank" 
             class="bg-[#1DB954] text-black px-8 py-3 rounded-full font-bold hover:scale-105 active:scale-95 transition-all shadow-lg hover:shadow-[#1DB954]/20 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
            Tải Bản .EXE
          </a>
          <a href="https://github.com/hoangtung-lux/Lossless-Downloader" target="_blank" 
             class="border border-[#b3b3b3] text-white px-8 py-3 rounded-full font-bold hover:bg-white/10 transition-all flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            Mã Nguồn
          </a>
        </div>
      </div>
      <div class="lg:w-1/2 mt-12 lg:mt-0 relative group">
        <div class="absolute -inset-4 bg-[#1DB954]/20 rounded-2xl blur-2xl group-hover:bg-[#1DB954]/30 transition-all duration-500"></div>
        <img src="https://raw.githubusercontent.com/hoangtung-lux/Lossless-Downloader/main/icon.jpg" 
             alt="Lumina Music Banner" 
             class="relative rounded-2xl border border-[#282828] shadow-2xl transform group-hover:rotate-1 group-hover:scale-[1.02] transition-all duration-500 w-full object-cover aspect-square md:aspect-video"/>
      </div>
    </section>

    <!-- Features Section -->
    <section class="max-w-6xl mx-auto py-20 px-6">
      <h2 class="text-3xl font-bold mb-12 text-center decoration-[#1DB954] underline-offset-8 underline decoration-4">Sức Mạnh Thực Sự</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div v-for="feature in features" :key="feature.title" 
             class="bg-[#181818] p-8 rounded-2xl border border-[#282828] hover:border-[#1DB954]/50 transition-all duration-300 hover:-translate-y-2 flex flex-col items-center text-center group">
          <div class="w-16 h-16 bg-[#1DB954]/10 rounded-full flex items-center justify-center mb-6 group-hover:bg-[#1DB954]/20 transition-colors shadow-inner">
            <component :is="feature.icon" class="w-8 h-8 text-[#1DB954]" />
          </div>
          <h3 class="text-xl font-bold mb-3">{{ feature.title }}</h3>
          <p class="text-[#b3b3b3] leading-relaxed">{{ feature.desc }}</p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-12 border-t border-[#282828] text-center text-[#b3b3b3] text-sm">
      <p>Made with ❤️ by <span class="text-white font-bold uppercase tracking-widest">hoangtung-lux</span> for J2TEAM Community</p>
      <div class="mt-4 flex justify-center items-center gap-6">
        <a href="https://github.com/hoangtung-lux/Lossless-Downloader" class="hover:text-white">GitHub</a>
        <a href="https://vibe.j2team.org" class="hover:text-white">Home Vibe</a>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const features = [
  {
    title: 'Smart Routing',
    desc: 'Tự động phân phối luồng tải Tidal/Qobuz/Deezer hay YouTube cực kỳ thông minh.',
    icon: 'ZapIcon'
  },
  {
    title: 'Hi-Fi Quality',
    desc: 'Hỗ trợ tải định dạng lossless FLAC thật sự, giữ trọn vẹn chất âm nguyên bản.',
    icon: 'MusicIcon'
  },
  {
    title: 'Modern UI',
    desc: 'Giao diện lấy cảm hứng từ Spotify, mượt mà và trực quan đến từng pixel.',
    icon: 'LayoutIcon'
  }
]

// Simple inline icons for accessibility
const ZapIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-zap"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>`
}
const MusicIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-music"><path d="M9 18V5l12-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle></svg>`
}
const LayoutIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-layout"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>`
}
</script>

<style>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.8s ease-out forwards;
}
</style>
