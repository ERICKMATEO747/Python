// Service Worker para notificaciones push de Flevo

self.addEventListener('push', function(event) {
    if (event.data) {
        const data = event.data.json();
        
        const options = {
            body: data.body,
            icon: data.icon || '/icon-192x192.png',
            badge: '/badge-72x72.png',
            data: {
                url: data.url_action || '/',
                ...data.data
            },
            actions: [
                {
                    action: 'open',
                    title: 'Abrir'
                },
                {
                    action: 'close',
                    title: 'Cerrar'
                }
            ],
            requireInteraction: true,
            tag: data.data?.type || 'flevo-notification'
        };
        
        event.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    }
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    
    if (event.action === 'open' || !event.action) {
        const url = event.notification.data.url || '/';
        
        event.waitUntil(
            clients.matchAll({ type: 'window' }).then(function(clientList) {
                // Si ya hay una ventana abierta, enfocarla
                for (let i = 0; i < clientList.length; i++) {
                    const client = clientList[i];
                    if (client.url.includes(url) && 'focus' in client) {
                        return client.focus();
                    }
                }
                
                // Si no hay ventana abierta, abrir una nueva
                if (clients.openWindow) {
                    return clients.openWindow(url);
                }
            })
        );
    }
});

self.addEventListener('notificationclose', function(event) {
    console.log('Notificación cerrada:', event.notification.tag);
});