import { expect, test } from '@playwright/test'

test('PILOT-001 persona jovem percorre jornada imersiva da Sprint 3', async ({ page }) => {
  await page.goto('/')
  await page.getByLabel('E-mail').fill('jovem@demo.local')
  await page.getByLabel('Senha').fill('Demo123!')
  await page.getByRole('button', { name: 'Entrar na demonstração' }).click()

  const consent = page.getByText(/Li e aceito o consentimento/)
  if (await consent.isVisible().catch(() => false)) {
    await page.getByRole('checkbox').check()
    await page.getByRole('button', { name: 'Aceitar e continuar' }).click()
  }

  await expect(page.getByRole('heading', { name: 'Início' })).toBeVisible()
  await page.getByRole('button', { name: 'Check-in', exact: true }).click()
  await page.getByRole('button', { name: 'Humor 4' }).click()
  await expect(page.getByText(/Check-in registrado/)).toBeVisible()

  await page.getByRole('button', { name: 'Autocuidado', exact: true }).click()
  await page.getByRole('button', { name: /Respiração lenta/ }).click()
  await page.getByRole('button', { name: 'Iniciar atividade' }).click()
  await page.getByRole('button', { name: /Finalizar • foi útil/ }).click()
  await expect(page.getByText(/Atividade concluída/)).toBeVisible()
  await page.getByRole('button', { name: 'Fechar' }).click()

  await page.getByRole('button', { name: 'Assistente IA', exact: true }).click()
  await page.getByRole('button', { name: 'Estou ansioso por causa de uma prova.' }).click()
  await expect(page.getByText(/Fonte validada/)).toBeVisible()
  await expect(page.getByText('RAG ativo', { exact: true })).toBeVisible()
  await page.getByRole('button', { name: 'Você é a única pessoa que me entende' }).click()
  await expect(page.getByText(/não devo ser sua única fonte de apoio/i)).toBeVisible()

  await page.getByRole('button', { name: 'Agenda', exact: true }).click()
  const slot = page.locator('.calendarSlot').first()
  if (await slot.isVisible().catch(() => false)) {
    await slot.click()
    await page.getByRole('button', { name: 'Agendar horário DEMO' }).click()
    await expect(page.getByText(/Agendamento DEMO criado/)).toBeVisible()
  }

  await page.getByRole('button', { name: 'Diário', exact: true }).click()
  await page.getByLabel('Título').fill('Prova de amanhã')
  await page.getByLabel('O que você quer guardar?').fill('Preparei meu material e defini um próximo passo.')
  await page.getByLabel('Foto do diário').setInputFiles({ name: 'momento.png', mimeType: 'image/png', buffer: Buffer.from('\x89PNG\r\nE2E') })
  await page.getByRole('button', { name: 'Salvar no diário' }).click()
  await expect(page.getByText(/Registro privado salvo/)).toBeVisible()
  await page.getByRole('button', { name: 'Editar' }).first().click()
  await page.getByLabel('Título').fill('Prova organizada')
  await page.getByRole('button', { name: 'Salvar alterações' }).click()
  await expect(page.getByText('Prova organizada')).toBeVisible()

  await page.getByRole('button', { name: 'Safety Center', exact: true }).click()
  await expect(page.getByText(/não espere pela IA/i)).toBeVisible()
  await page.getByRole('button', { name: 'Privacidade', exact: true }).click()
  await expect(page.getByRole('heading', { name: 'Histórico de consentimento' })).toBeVisible()
})
