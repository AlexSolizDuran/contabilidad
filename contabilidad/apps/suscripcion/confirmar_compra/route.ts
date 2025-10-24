import { proxyToBackend } from "@/lib/proxyRequest";
import { NextRequest, NextResponse } from "next/server";

// Este proxy redirige la solicitud POST a Django
// La URL completa en Django es: /suscripcion/confirmar_compra/
async function handler(req:NextRequest):Promise<NextResponse> {
    return proxyToBackend(req,'suscripcion/confirmar_compra') 
}

export const POST = handler;
